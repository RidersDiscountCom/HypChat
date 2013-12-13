from __future__ import absolute_import, division
import json
from .requests import Requests, BearerAuth
from .restobject import Linker


class _requests(Requests):
	@staticmethod
	def _data(data, kwargs):
		if isinstance(data, basestring):
			return data
		elif data is not None:
			kwargs.setdefault('headers',{})['Content-Type'] = 'application/json'
			return json.dumps(data)

	def request(self, method, url, **kwargs):
		rv = super(_requests, self).request(method, url, **kwargs)
		# TODO: If we've reached our rate limit: raise warning, sleep, and try again

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
		self.users = Linker('https://api.hipchat.com/v2/user', _requests=self._requests)

	def fromurl(self, url):
		return Linker(url, _requests=self._requests)()

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

	def get_room(self, id_or_name):
		return self.fromurl('https://api.hipchat.com/v2/room/%s' % id_or_name)

	def get_user(self, id_or_email):
		return self.fromurl('https://api.hipchat.com/v2/user/%s' % id_or_email)

	def get_emoticon(self, id_or_shortcut):
		return self.fromurl('https://api.hipchat.com/v2/emoticon/%s' % id_or_shortcut)
