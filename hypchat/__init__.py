from __future__ import absolute_import, division
from .requests import Requests, BearerAuth

class _requests(Requests):
	@staticmethod
	def _data(data, kwargs):
		if isinstance(data, basestring):
			return data
		elif data is not None:
			kwargs.setdefault('headers',{})['Content-Type'] = 'application/json'
			return json.dumps(data)

	def post(self, url, data=None, **kwargs):
		data = self._data(data, kwargs)
		return self.requests.post(url, data, **self._kw(kwargs))
		
	def patch(self, url, data=None, **kwargs):
		data = self._data(data, kwargs)
		return self.requests.patch(url, data, **self._kw(kwargs))
		
	def put(self, url, data=None, **kwargs):
		data = self._data(data, kwargs)
		return self.requests.put(url, data, **self._kw(kwargs))

from .jsonobject import Linker

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
		return Linker._obj_from_text(resp.text)
