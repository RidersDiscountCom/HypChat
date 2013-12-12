=======
HypChat
=======
A Python package for HipChat's v2 JSON REST API. It's based on v2's navigability and self-declaration.

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

Other Actions
~~~~~~~~~~~~~

Many of the v2 types define additional types, eg Rooms have methods for messaging, setting the topic, getting the history, and inviting users to the room. These are implemented as methods of subclasses. The complete listing is in the `Type List`_.

Usage
=====

First, create a HypChat object with the token

::

	hc = HypChat("mytoken")

There are several root links

Type List
=========
TODO