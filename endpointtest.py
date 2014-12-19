import os
import ConfigParser
import sys
from hypchat import *

AUTH_TOKEN = None
ENDPOINT = None
config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.hypchat'), '/etc/hypchat'])
if config.has_section('HipChat'):
    AUTH_TOKEN = config.get('HipChat', 'token')
    ENDPOINT = config.get('HipChat', 'endpoint')

if 'HIPCHAT_TOKEN' in os.environ:
    AUTH_TOKEN = os.environ['HIPCHAT_TOKEN']

if 'HIPCHAT_ENDPOINT' in os.environ:
    ENDPOINT = os.environ['HIPCHAT_ENDPOINT']

if ENDPOINT:
    hipchat = HypChat(AUTH_TOKEN, ENDPOINT)
else:
    hipchat = HypChat(AUTH_TOKEN)

import datetime

room = hipchat.rooms()['items'][0]
print(room['name'])
