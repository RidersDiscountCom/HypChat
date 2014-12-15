import unittest
import time
import requests_mock

from common import TestHypChat

class TestRateLimit(TestHypChat):
  def setUp(self):
    super(TestRateLimit, self).setUp()
    self.call_counter = 1

  def successfull_callback(self, request, context):
    context.status_code = 200

    headers = {
        'X-Ratelimit-Limit': '100',
        'X-Ratelimit-Remaining': '99',
        'X-Ratelimit-Reset': str(time.time())
    }

    context.headers = headers

    payload = {
      'atlassian_id': None,
      'created': '2014-09-26T10:44:04+00:00',
      'email': 'john.doe@example.com',
      'group': None,
      'id': 12345,
      'is_deleted': False,
      'is_group_admin': True,
      'is_guest': False,
      'last_active': str(int(time.time())),
      'links': {
          'self': 'https://api.hipchat.com/v2/user/12345'
      },
      'mention_name': 'john',
      'name': 'John Doe',
      'photo_url': 'https://s3.amazonaws.com/uploads.hipchat.com/photos/12345/ABCDEFG.jpg',
      'presence': {
          'client': {
              'type': 'http://hipchat.com/client/mac',
              'version': '12345'
          },
          'is_online': True
      },
      'timezone': 'Europe/Berlin',
      'title': 'Software Engineer',
      'xmpp_jid': '12345@chat.hipchat.com'
    }

    return payload

  def rate_limited_callback(self, request, context):
    context.status_code = 429

    headers = {
        'X-Ratelimit-Limit': '100',
        'X-Ratelimit-Remaining': '0',
        'X-Ratelimit-Reset': str(time.time() + 0.1)
    }

    context.headers = headers

    payload = {
      'error': {
        'code': 429,
        'type': 'Too Many Requests',
        'message': 'Rate Limit exceeded'
      }
    }

    return payload

  def hipchat_callback(self, request, context):
    rate_limit = self.call_counter % 2 == 0 
    self.call_counter += 1

    if rate_limit:
      return self.rate_limited_callback(request, context)
    else:
      return self.successfull_callback(request, context)

    

  def runTest(self):
    """
    We are mocking the request so every second call is rate limited. 
    """
    with requests_mock.Mocker() as m:
      m.register_uri('GET', 'https://api.hipchat.com/v2/user/@john', status_code=200, json=self.hipchat_callback)
      for i in xrange(3):
        self.hipchat.get_user('@john')