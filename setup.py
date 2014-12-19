#!/usr/bin/env python

from distutils.core import setup, Command

class PyTest(Command):
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    import sys, subprocess
    errno = subprocess.call([sys.executable, '-m', 'unittest', 'discover'])
    raise SystemExit(errno)

def read_file(name):
    """
    Read file content
    """
    f = open(name)
    try:
        return f.read()
    except IOError:
        print("could not read %r" % name)
        f.close()

setup(name='hypchat',
      version='0.18',
      description="Package for HipChat's v2 API",
      long_description=read_file('README.rst'),
      author='Riders Discount',
      author_email='opensource@ridersdiscount.com',
      url='https://github.com/RidersDiscountCom/HypChat',
      packages=['hypchat'],
      install_requires=['requests', 'python-dateutil', 'six'],
      test_requires=['requests_mock'],
      provides=['hypchat'],
      cmdclass= { 'test': PyTest },
      classifiers=[ # https://pypi.python.org/pypi?%3Aaction=list_classifiers
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: Communications :: Chat',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
      ]
     )
