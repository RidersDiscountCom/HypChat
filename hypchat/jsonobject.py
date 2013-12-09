from __future__ import absolute_import, division
import json
from . import requests

class Linker(object):
	"""
	Responsible for on-demand loading of JSON objects.
	"""
	def __init__(self, url, parent=None, _requests=None):
		self.url = url
		self.__parent = parent
		self._requests = _requests or __import__('requests')

	def __call__(self):
		def _object_hook(obj):
			if 'links' in obj:
				rv = JsonObject(obj)
				rv._requests = self._requests
				return rv
			else:
				return obj

		rv = json.JSONDecoder(object_hook=_object_hook).decode(self._requests.get(self.url).text)
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

	def save(self):
		return requests.put(self['links']['self']).json()
