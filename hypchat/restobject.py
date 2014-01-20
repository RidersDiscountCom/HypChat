from __future__ import absolute_import, division
import json
import re
import datetime
import dateutil.parser
import dateutil.tz

_urls_to_objects = {}

def timestamp(dt):
	"""
	Parses a HipChat datetime value.

	HipChat uses ISO 8601, optionally with the timezone attached. Except for when they use a timestamp.
	"""
	#'2013-12-05T22:42:18+00:00' <== History
	#'2013-11-27T15:33:24' <== Rooms, Users
	if dt is None:
		return
	if isinstance(dt, int):
		rv = datetime.datetime.fromtimestamp(dt, dateutil.tz.tzutc())
	elif dt.isdigit():
		rv = datetime.datetime.fromtimestamp(int(dt), dateutil.tz.tzutc())
	else:
		rv = dateutil.parser.parse(dt)
	if rv.tzinfo is None:
		rv = rv.replace(tzinfo=dateutil.tz.tzutc())
	return rv

def mktimestamp(dt):
	"""
	Prepares a datetime for sending to HipChat.
	"""
	if dt.tzinfo is None:
		dt = dt.replace(tzinfo=dateutil.tz.tzutc())
	return dt.isoformat(), dt.tzinfo.tzname(dt)

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
				klass = RestObject
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

class RestObject(dict):
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
		return self._requests.put(self.url, data=self).json()

	def delete(self):
		self._requests.delete(self.url)


class Room(RestObject):
	def __init__(self, *p, **kw):
		super(Room, self).__init__(*p, **kw)
		if 'last_active' in self:
			self['last_active'] = timestamp(self['last_active'])
		if 'created' in self:
			self['created'] = timestamp(self['created'])

	def save(self):
		data = {}
		for key in ('name', 'privacy', 'is_archived', 'is_guest_accessible', 'topic'):
			data[key] = self[key]
		data['owner'] = {
			'id': self['owner']['id']
		}
		self._requests.put(self.url, data=data)

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

	def history(self, date='recent', maxResults=200):
		tz = 'UTC'
		if date != 'recent':
			date, tz = mktimestamp(date)
		params = {
			'date':date, 
			'timezone': tz, 
			'max-results': maxResults,
		}
		resp = self._requests.get(self.url+'/history', params=params)
		return Linker._obj_from_text(resp.text, self._requests)

	def invite(self, user, reason):
		self._requests.post(self.url+'/invite/%s' % user['id'], data={
			'reason': reason,
		})

	def create_webhook(self, url, event, pattern=None, name=None):
		"""
		Creates a new webhook.
		"""
		data={
			'url': url,
			'event': event,
			'pattern': pattern,
			'name': name,
		}
		resp = self._requests.post(self.url+'/webhook', data=data)
		return Linker._obj_from_text(resp.text, self._requests)

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/room/[^/]+$')] = Room

class User(RestObject):
	def __init__(self, *p, **kw):
		super(User, self).__init__(*p, **kw)
		if 'last_active' in self:
			self['last_active'] = timestamp(self['last_active'])
		if 'created' in self:
			self['created'] = timestamp(self['created'])

	def message(self, message):
		"""
		Sends a user a private message.
		"""
		self._requests.post(self.url+'/message', data={
			'message': message,
		})

	def save(self):
		data = {}
		for key, value in self.iteritems():
			if key == 'presence' and isinstance(value, dict):
				p = {}
				for k,v in value.iteritems():
					if k in ('status', 'show'):
						p[k] = v
				if len(p) != 0:
					data[key] = p
			else:
				data[key] = value
		return self._requests.put(self.url, data=data).json()

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/user/[^/]+$')] = User

class Collection(object):
	"""
	Mixin for collections
	"""
	def contents(self, **kwargs):
		page = self
		ops = {}
		if kwargs.get('expand'):
			ops['expand'] = 'items'
		while hasattr(page, 'next'):
			for item in page['items']:
				yield item
			page = page.next(**ops)
		# Last page handling
		for item in page['items']:
			yield item


class MemberCollection(RestObject, Collection):
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

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/room/[^/]+/member$')] = MemberCollection

class UserCollection(RestObject, Collection):
	def create(self, name, email, title=None, mention_name=None, is_group_admin=False, timezone='UTC', password=None):
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
		resp = self._requests.post(self.url, data=data)
		return Linker._obj_from_text(resp.text, self._requests)

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/user$')] = UserCollection

class RoomCollection(RestObject, Collection):
	def create(self, name, owner=Ellipsis, privacy='public', guest_access=True):
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
		resp = self._requests.post(self.url, data=data)
		return Linker._obj_from_text(resp.text, self._requests)

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/room$')] = RoomCollection

class WebhookCollection(RestObject, Collection):
	def create(self, url, event, pattern=None, name=None):
		"""
		Creates a new webhook.
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
		resp = self._requests.post(self.url, data=data)
		return Linker._obj_from_text(resp.text, self._requests)

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/room/[^/]+/webhook$')] = WebhookCollection

class EmoticonCollection(RestObject, Collection):
	pass

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/emoticon$')] = EmoticonCollection

class Webhook(RestObject):
	def __init__(self, *p, **kw):
		super(Webhook, self).__init__(*p, **kw)
		if 'created' in self:
			self['created'] = timestamp(self['created'])

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/room/[^/]+/webhook/[^/]+$')] = Webhook


class HistoryCollection(RestObject, Collection):
	def __init__(self, *p, **kw):
		super(HistoryCollection, self).__init__(*p, **kw)
		for item in self['items']:
			if 'date' in item:
				item['date'] = timestamp(item['date'])

_urls_to_objects[re.compile(r'^https://api.hipchat.com/v2/room/[^/]+/history$')] = HistoryCollection
