=======
HypChat
=======
A Python package for HipChat's `v2 JSON REST API`_. It's based on v2's navigability and self-declaration.

.. _v2 JSON REST API: https://www.hipchat.com/docs/apiv2

Installation
============
HypChat can either be installed from PyPI_:
::

	pip install hypchat

Or from source:
::

	python setup.py install

.. _PyPI: https://pypi.python.org/pypi/hypchat/

Concepts
========

There are two basic types in HypChat: ``Linker`` and ``RestObject``. They are not meant to be instantiated directly but instead created as references from other objects.

Linker
------
A simple callable that represents an unfollowed reference.

``l.url``
	The URL this object points to

``l()``
	Calling a ``Linker`` will perform the request and return a ``RestObject``

RestObject
----------
A subclass of ``dict``, contains additional functionality for links and actions.

Links
~~~~~
As part of the v2 API, all objects have a ``links`` property with references to other objects. This is used to create ``Linker`` objects as attributes.

For example, all objects have a link called ``self``. This may be referenced as:
::

	obj.self

And the request performed by calling it:
::

	obj.self()

.. _expand:

If `Title Expansion`_ is desired, just past a list of things to be expanded as the ``expand`` keyword argument.

.. _Title Expansion: https://www.hipchat.com/docs/apiv2/expansion

Other Actions
~~~~~~~~~~~~~

Many of the v2 types define additional types, eg Rooms have methods for messaging, setting the topic, getting the history, and inviting users to the room. These are implemented as methods of subclasses. The complete listing is in the `Type List`_.

Timezone Handling
-----------------
HypChat uses aware ``datetime`` objects throughout by the ``dateutil`` module. However, the HipChat API universally uses UTC.

For methods that take a ``datetime``, if a naive object is given, it will be assumed to be in UTC. If this is not what you mean, ``dateutil.tz`` has a wonderful selection of timezones_ available.

.. _timezones: http://labix.org/python-dateutil#head-587bd3efc48f897f55c179abc520a34330ee0a62

Usage
=====

First, create a HypChat object with the token

::

	hc = HypChat("mytoken")

There are several root links:

::

	rooms = hc.rooms()
	users = hc.users()
	emots = hc.emoticons()
	caps = hc.capabilities()

In addition, the HypChat object has methods for creating objects and directly referencing the basic types.

For example, you might do:

::
	for room in (r for r in hipchat.rooms(expand='items') if r['last_active'] < datetime.datetime(2013, 12, 1)):
		room.owner.message("Your room is dead; maybe archive it")

Since ``room.owner`` is a User_ stub, not just a generic object. (The Room_ objects are not stubs, since the ``expand`` keyword is used).

Downloading history is as easy as:

::
	list(HypChat(token).get_room(id).history(datetime.datetime.utcnow()).contents())

Note that this may eat up many requests for large rooms.

Navigation
----------
Any time an object is referenced in a value (eg ``room['owner']``), a stub of that object is created, and the full object may be found with ``.self()``. Stubs contain the ID of the object, the name (if applicable), and any links that object has—including ``self``. This can be avoided by using the expand_ keyword.

Collections—such as ``rooms``, ``users``, and ``emots`` above—all have an ``'items'`` key containing their list of things. In addition, the ``.contents()`` method will generate all of the items, handling pagination. As usual, object

Console
-------
If you call ``python -m hypchat``, a interactive prompt (using IPython_ if available) will appear. The environment will contain ``hipchat``, an instance of the ``HypChat`` object. The token is pulled from ``~/.hypchat``, ``/etc/hypchat``, or the environment variable ``HIPCHAT_TOKEN``.

.. _IPython: http://ipython.org/

Type List
=========

See `TYPES.rst`_

.. _TYPES.rst: https://github.com/RidersDiscountCom/HypChat/blob/master/TYPES.rst

TODO List
=========
* API Links
* Rate Limit handling