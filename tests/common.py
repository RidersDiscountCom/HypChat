import unittest
import sys
import os, os.path
import ConfigParser

package = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, package)

import hypchat


class TestHypChat(unittest.TestCase):
    def setUp(self):
        self.setUpConfig()
        self.setUpHipChat()

    def setUpConfig(self):
        search_paths = [os.path.expanduser('~/.hypchat'), '/etc/hypchat']

        self.config = ConfigParser.ConfigParser()
        self.config.read(search_paths)
        if self.config.has_section('HipChat'):
            self.access_token = self.config.get('HipChat', 'token')
        elif 'HIPCHAT_TOKEN' in os.environ:
            self.access_token = os.environ['HIPCHAT_TOKEN']
        else:
            print('Authorization token not detected! The token is pulled from ' \
                  '~/.hypchat, /etc/hypchat, or the environment variable HIPCHAT_TOKEN.')

    def setUpHipChat(self):
        self.hipchat = hypchat.HypChat(self.access_token)