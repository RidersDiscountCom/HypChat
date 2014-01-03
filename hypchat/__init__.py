from __future__ import absolute_import, division
import json
import time
import warnings
import sys
import os
import datetime
from .requests import Requests, BearerAuth, HttpForbidden
from .restobject import Linker

class RateLimitWarning(Warning):
	"""
	This token has been rate limited. Waiting for the next reset.
	"""

def jsonify(obj):
	if isinstance(obj, datetime.datetime):
		return obj.isoformat()
	elif isinstance(obj, set):
		return list(obj)
	else:
		raise TypeError("Can't JSONify objects of type %s" % type(obj).__name__)

class _requests(Requests):
	def __init__(self, *p, **kw):
		super(_requests, self).__init__(*p, **kw)
		self.rl_remaining = 99999
		self.rl_reset = 0
		self.dump_reqs = '__HYPCHAT_DEBUG_REQUESTS__' in os.environ

	@staticmethod
	def _data(data, kwargs):
		if isinstance(data, basestring):
			return data
		elif data is not None:
			kwargs.setdefault('headers',{})['Content-Type'] = 'application/json'
			rv = json.dumps(data, default=jsonify)
			print rv
			return rv

	def _rl_sleep(self, until):
		t = until - time.time()
		if t > 0:
			warnings.warn("HipChat has been rate limited; Waiting %0.1fs for the next reset." % t, RateLimitWarning)
			time.sleep(t)

	def request(self, method, url, **kwargs):
		if self.dump_reqs:
			print >> sys.stderr, "REQUEST", method, url
		while True:
			try:
				if self.rl_remaining <= 0:
					# We're out of requests, chill
					self._rl_sleep(self.rl_reset)
				resp = super(_requests, self).request(method, url, **kwargs)
			except HttpForbidden, e:
				#FIXME: Is there a better way to do this?
				if e.response.json()['error']['message'] == u'You have exceeded the rate limit. See https://www.hipchat.com/docs/api/rate_limiting':
					self.rl_remaining = int(e.response.headers['x-ratelimit-remaining'])
					self.rl_reset = float(e.response.headers['x-ratelimit-reset'])
					continue # Try the request again
				else:
					raise
			else:
				self.rl_remaining = int(resp.headers['x-ratelimit-remaining'])
				self.rl_reset = float(resp.headers['x-ratelimit-reset'])
				return resp

	def post(self, url, data=None, **kwargs):
		data = self._data(data, kwargs)
		return super(_requests, self).post(url, data=data, **kwargs)
		
	def patch(self, url, data=None, **kwargs):
		data = self._data(data, kwargs)
		return super(_requests, self).patch(url, ddata=ata, **kwargs)
		
	def put(self, url, data=None, **kwargs):
		data = self._data(data, kwargs)
		return super(_requests, self).put(url, data=data, **kwargs)


__all__ = ('HypChat',)

class HypChat(object):
	def __init__(self, token):
		self._requests = _requests(auth=BearerAuth(token))
		self.capabilities = Linker('https://api.hipchat.com/v2/capabilities', _requests=self._requests)
		self.emoticons = Linker('https://api.hipchat.com/v2/emoticon', _requests=self._requests)
		self.rooms = Linker('https://api.hipchat.com/v2/room', _requests=self._requests)

	def users(self, **ops):
		"""users([guests=bool], [deleted=bool]) -> UserCollection

		Returns a collection of users, with the following keyword options:
		* guests: If True, return active guests
		* deleted: If True, return deleted users
		"""
		params = {}
		if ops.get('guests', False):
			params['include-guests'] = 'true'
		if ops.get('deleted', False):
			params['include-deleted'] = 'true'
		resp = self._requests.get('https://api.hipchat.com/v2/user', params=params)
		return Linker._obj_from_text(resp.text, self._requests)


	def fromurl(self, url, **kwargs):
		return Linker(url, _requests=self._requests)(**kwargs)

	def create_room(self, name, owner=Ellipsis, privacy='public', guest_access=True):
		"""
		Creates a new room.
		"""
		data={
			'name': name,
			'privacy': privacy,
			'guest_access': guest_access,
		}
		if owner is not Ellipsis:
			if owner is None:
				data['owner_user_id'] = owner
			else:
				data['owner_user_id'] = owner['id']
		resp = self._requests.post(self.rooms.url, data=data)
		return Linker._obj_from_text(resp.text, self._requests)

	def create_user(self, name, email, title=None, mention_name=None, is_group_admin=False, timezone='UTC', password=None):
		"""
		Creates a new user.
		"""
		data={
			'name': name,
			'email': email,
			'title': title,
			'mention_name': mention_name,
			'is_group_admin': is_group_admin,
			'timezone': timezone, # TODO: Support timezone objects
			'password': password,
		}
		resp = self._requests.post(self.users.url, data=data)
		return Linker._obj_from_text(resp.text, self._requests)

	def get_room(self, id_or_name, **kwargs):
		return self.fromurl('https://api.hipchat.com/v2/room/%s' % id_or_name, **kwargs)

	def get_user(self, id_or_email, **kwargs):
		return self.fromurl('https://api.hipchat.com/v2/user/%s' % id_or_email, **kwargs)

	def get_emoticon(self, id_or_shortcut, **kwargs):
		return self.fromurl('https://api.hipchat.com/v2/emoticon/%s' % id_or_shortcut, **kwargs)
