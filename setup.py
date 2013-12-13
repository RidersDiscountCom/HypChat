#!/usr/bin/env python

from distutils.core import setup

setup(name='hypchat',
      version='0.4',
      description="Package for HipChat's v2 API",
      long_description=open('README.rst').read(),
      author='James Bliss',
      author_email='james@ridersdiscount.com',
      url='https://github.com/RidersDiscountCom/HypChat',
      packages=['hypchat'],
      requires=['requests', 'dateutil'],
      provides=['hypchat'],
      classifiers=[ # https://pypi.python.org/pypi?%3Aaction=list_classifiers
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2 :: Only',
            'Topic :: Communications :: Chat',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
      ]
     )