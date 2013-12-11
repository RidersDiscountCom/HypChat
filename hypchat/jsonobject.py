from __future__ import absolute_import, division
import json
import re

_urls_to_objects = {}

class Linker(object):
	"""
	Responsible for on-demand loading of JSON objects.
	"""
	url = None
	def __init__(self, url, parent=None, _requests=None):
		self.url = url
		self.__parent = parent
		self._requests = _requests or __import__('requests')

	@staticmethod
	def _obj_from_text(text, requests):
		"""
		Constructs objects (including our wrapper classes) from a JSON-formatted string
		"""
		def _object_hook(obj):
			if 'links' in obj:
				klass = JsonObject
				if 'self' in obj['links']:
					for p, c in _urls_to_objects.iteritems():
						if p.match(obj['links']['self']):
							klass = c
							break
				rv = klass(obj)
				rv._requests = requests
				return rv
			else:
				return obj
		return json.JSONDecoder(object_hook=_object_hook).decode(text)

	def __call__(self, expand=None):
		"""
		Actually perform the request
		"""
		params = None
		if expand is not None:
			if isinstance(expand, basestring):
				params = {'expand': expand}
			else:
				params = {'expand': ','.join(expand)}

		rv = self._obj_from_text(self._requests.get(self.url, params=params).text, self._requests)
		rv._requests = self._requests
		if self.__parent is not None:
			rv.parent = self.__parent
		return rv

	def __repr__(self):
		return "<%s url=%r>" % (type(self).__name__, self.url)

class JsonObject(dict):
	"""
	Nice wrapper around the JSON objects and their links.
	"""
	def __getattr__(self, name):
		if name in self.get('links', {}):
			return Linker(self['links'][name], parent=self, _requests=self._requests)
		elif name in self:
			return self[name]
		else:
			raise AttributeError("%r object has no attribute %r" % (type(self).__name__, name))

	@property
	def url(self):
		return self['links']['self']

	def save(self):
		return self._requests.put(self.url).json()

	def delete(self):
		return self._requests.delete(self.url).json()


class Room(JsonObject):
	def message(self, *p, **kw):
		"""
		Redirects to the /notification URL.

		Will soon be reimplemented as a resource that posts a message to a room as a user.
		"""
		return self.notification(*p, **kw)

	def notification(self, message, color='yellow', notify=False, format='html'):
		"""
		Send a message to a room.
		"""
		self._requests.post(self.url+'/notification', data={
			'color': color,
			'message': message,
			'notify': notify,
			'message_format': format,
		})

	def topic(self, text):
		"""
		Set a room's topic. Useful for displaying statistics, important links, server status, you name it!
		"""
		self._requests.put(self.url+'/topic', data={
			'topic': text,
		})

	def history(self, date='recent'):
		# TODO: If given an aware datetime, pass its timezone along
		raise NotImplementedError

	def invite(self, user, reason):
		self._requests.post(self.url+'/invite/%s' % user['id'], data={
			'reason': reason,
		})


_urls_to_objects[re.compile(r'https://api.hipchat.com/v2/room/[^/]+')] = Room

class User(JsonObject):
	def message(self, message):
		raise NotImplementedError

_urls_to_objects[re.compile(r'https://api.hipchat.com/v2/user/[^/]+')] = User

class MemberCollection(JsonObject):
	def add(self, user):
		"""
		Adds a member to a private room.
		"""
		self._requests.put(self.url+'/%s' % user['id'])

	def remove(self, user):
		"""
		Removes a member from a private room.
		"""
		self._requests.delete(self.url+'/%s' % user['id'])

_urls_to_objects[re.compile(r'https://api.hipchat.com/v2/room/[^/]+/member')] = MemberCollection
