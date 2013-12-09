from __future__ import absolute_import, division
import requests

class BearerAuth(requests.auth.AuthBase):
	def __init__(self, token):
		self.token = token
	
	def __call__(self, r):
		r.headers['Authorization'] = "Bearer %s" % self.token
		return r

def req(method, url, params=None, data=None):
	c = getattr(requests, method.lower())
	kwargs = {}
	if params is not None:
		kwargs['params'] = params
	if data is not None:
		kwargs['headers'] = {'content-type': 'application/json'}
		kwargs['data'] = json.dumps(data)
	return c(url, auth=BearerAuth(AUTH_TOKEN), **kwargs)

class Requests(object):
	"""
	Class whose job is to provide defaults to the Requests module
	"""
	# Aliases to mimic the requests module
	from requests import (
		codes, session, Session, 
		RequestException, Timeout, URLRequired,
		TooManyRedirects, HTTPError, ConnectionError
	)
	
	# Set this if you want to forward to somebody else
	requests = __import__('requests')
	
	def __init__(self, **kwargs):
		self._template = kwargs.copy()
	
	def _kw(self, kwargs):
		kw = self._template.copy()
		kw.update(kwargs)
		return kw
	
	def request(self, method, url, **kwargs):
		return self.requests.request(method, url, **self._kw(kwargs))
	
	def get(self, url, **kwargs):
		return self.requests.get(url, **self._kw(kwargs))
		
	def head(self, url, **kwargs):
		return self.requests.head(url, **self._kw(kwargs))
		
	def post(self, url, data=None, **kwargs):
		return self.requests.post(url, data, **self._kw(kwargs))
		
	def patch(self, url, data=None, **kwargs):
		return self.requests.patch(url, data, **self._kw(kwargs))
		
	def put(self, url, data=None, **kwargs):
		return self.requests.put(url, data, **self._kw(kwargs))
		
	def delete(self, url, **kwargs):
		return self.requests.delete(url, **self._kw(kwargs))
		
	def options(self, url, **kwargs):
		return self.requests.options(url, **self._kw(kwargs))
