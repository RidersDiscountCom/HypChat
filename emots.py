#!/usr/bin/python
"""
Writes out emots.html, and index of all emoticons available to you.
"""

import os, os.path
import ConfigParser
import sys
from hypchat import *

config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.hypchat'), '/etc/hypchat'])
AUTH_TOKEN = config.get('HipChat', 'token')

hipchat = HypChat(AUTH_TOKEN)

with open('emots.html', 'w') as html:
    html.write("""
<!DOCTYPE html>
<html>
	<head>
		<title>HipChat Emoticons</title>
	</head>
	<body>
""")
    for emot in hipchat.emoticons().contents():
        html.write("""
<img src="{url}" alt="{shortcut}" title="{shortcut}">
""".format(**emot))

    html.write("""
	</body>
</html>""")