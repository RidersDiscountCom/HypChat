import os, os.path
import ConfigParser
import sys
from hypchat import *

config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.hypchat'), '/etc/hypchat'])
AUTH_TOKEN = config.get('HipChat', 'token')

if 'HIPCHAT_TOKEN' in os.environ:
    AUTH_TOKEN = os.environ['HIPCHAT_TOKEN']

hipchat = HypChat(AUTH_TOKEN)

import datetime

room = hipchat.rooms()['items'][0]
print room['name']
hist = room.history(datetime.datetime.utcnow(), maxResults=500)
fullhist = []
for item in hist.contents():
    print item['message']