=======
HypChat
=======
A Python package for HipChat's `v2 JSON REST API`_. It's based on v2's navigability and self-declaration.

.. _v2 JSON REST API: https://www.hipchat.com/docs/apiv2

Concepts
========

There are two basic types in HypChat: ``Linker`` and ``JsonObject``. They are not meant to be instantiated directly but instead created as references from other objects.

Linker
------
A simple callable that represents an unfollowed reference.

``l.url``
	The URL this object points to

``l()``
	Calling a ``Linker`` will perform the request and return a ``JsonObject``

JsonObject
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

Navigation
----------
Any time an object is referenced in a value (eg ``room['owner']``), a stub of that object is created, and the full object may be found with ``.self()``. Stubs contain the ID of the object, the name (if applicable), and any links that object has—including ``self``. This can be avoided by using the expand_ keyword.

Collections—such as ``rooms``, ``users``, and ``emots`` above—all have an ``'items'`` key containing their list of things. In addition, the ``.contents()`` method will generate all of the items, handling pagination. As usual, object

Console
-------
If you call ``python -m hypchat``, a interactive prompt (using IPython_ if available) will appear. The environment will contain ``hipchat``, an instance of the ``HypChat`` object. The token is pull from ``~/.hypchat``, ``/etc/hypchat``, or the environment variable ``HIPCHAT_TOKEN``.

.. _IPython: http://ipython.org/

Type List
=========

HypChat
-------
As the root object, this is mostly full of "singletons" and shortcut methods.

Links
~~~~~
``capabilities``
	The `capabilities descriptor`_ for HipChat

``emoticons``
	The `Emoticons Collection`_

``rooms``
	The `Rooms Collection`_

``users``
	The `Users Collection`_

.. _capabilities descriptor: https://www.hipchat.com/docs/apiv2/method/get_capabilities

Methods
~~~~~~~
``create_user()``
	Creates a new User_ object and returns the response.

``get_user()``
	Gets a User_ directly without having to navigate

``create_room()``
	Creates a new Room_ object and returns the response.

``get_room()``
	Gets a Room_ directly without having to navigate

``get_emoticon()``
	Gets a Emoticon_ directly without having to navigate

JSON Objects
------------
All objects, collections, rooms, webhooks, etc have these things.

Links
~~~~~
``self``
	A link to this object

Values
~~~~~~
``id``
	The numeric ID of this object (except collections and webhooks)

All Collections
---------------
All collections share this interface. Specific collection objects are "paged": no single object contains all items.

Links
~~~~~
``next``
	(Optional) The next page in this collection
``prev``
	(Optional) The previous page in this collection

Values
~~~~~~
``items``
	A list of the things for this 'page' of the collection

``maxResults``
	The maximum number of items that could be in this page

``startIndex``
	The index of the first item in this page, starting at 0

Methods
~~~~~~~
``contents()``
	A generator that produces all items, navigating pagination in the process

Rooms Collection
----------------
In addition to the things defined in `All Collections`_, the Rooms Collection has the below.

Methods
~~~~~~~
``create()``
	Creates a new Room_

Room
----
Representing a single chat room.

Links
~~~~~
``webhooks``
	The `Webhooks Collection`_ for this room

``members``
	(Optional) For private rooms only; the `Members Collection`_ for this room

Methods
~~~~~~~
``message()``
	Currently a pointer to ``notification()``

``notification()``
	Sends a message to a room

``topic()``
	Sets the topic

.. ``history()``
	Grabs a "collection" of the history

``invite()``
	Invite a user to this room

Values
~~~~~~
``name``
	Display name

``created``
	When the room was created

``guest_access_url``
	The URL to give for guest access, if enabled

``is_archived``
	``True`` if this room is archived, ``False`` otherwise

``last_active``
	When the room last had activity

``owner``
	A reference to the owning User_

``participants``
	A list of User_ stubs currently in the room

``privacy``
	One of ``'public'`` or ``'private'``

``topic``
	The current topic

``xmpp_jid``
	The XMPP (Jabber) ID

Webhooks Collection
-------------------
In addition to the those in `All Collections`_, the Webhooks Collection has the below.

Methods
~~~~~~~
``create()``
	Create a new webhook

Members Collection
------------------
In addition to the those in `All Collections`_, the Members Collection has the below.

Methods
~~~~~~~
``add()``
	Add a User_ to the list of members

``remove()``
	Remove a User_ from the list of members

Users Collection
----------------
In addition to the things defined in `All Collections`_, the Users Collection has the below.

Methods
~~~~~~~
``create()``
	Creates a new User_

User
----
TODO

Emoticons Collection
--------------------
TODO

Emoticon
--------
TODO

TODO List
=========
* Proper Datetime and Timezone (dateutils) support
* API Links