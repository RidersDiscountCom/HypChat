from . import *
import os, os.path
import ConfigParser

config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.hypchat'), '/etc/hypchat'])
AUTH_TOKEN = config.get('HipChat', 'token')

if 'HIPCHAT_TOKEN' in os.environ:
	AUTH_TOKEN = os.environ['HIPCHAT_TOKEN']

hipchat = HypChat(AUTH_TOKEN)

capabilities = hipchat.capabilities
emoticons = hipchat.emoticons
rooms = hipchat.rooms
users = hipchat.users

try:
	import IPython
	IPython.embed()
except ImportError:
	import code
	code.interact(local=locals())