======================
HypChat Type Reference
======================

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

REST Objects
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

Methods
~~~~~~~
``delete()``
	Attempts to delete the object (with HTTP ``DELETE``)

``save()``
	Attempts to save the object (with HTTP ``PUT``)

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
	Create a new Webhook_

Webhook
-------
Unlike most REST Objects, Webhooks don't have an ID. Their stub is also much more extensive

Fields
~~~~~~
``url``
	(Stubbed) The URL to ``POST`` to

``event``
	(Stubbed) The event to call this hook on, one of ``'room_message'``, ``'room_notification'``, ``'room_exit'``, ``'room_enter'``, ``'room_topic_change'``

``pattern``
	(Stubbed) When ``event`` is ``'room_message'``, a regular expression to match against the message

``name``
	(Stubbed) A human label for this hook

``room``
	The Room_ this webhook is for

``creator``
	The User_ that created this webhook

``created``
	When this webhook was created

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

Methods
~~~~~~~
``message()``
	Sends a private message to the given user

Values
~~~~~~
``name``
	Display name

``xmpp_jid``
	The XMPP (Jabber) ID of the user

``is_deleted``
	``True`` if the user has been deleted

``last_active``
	The last time the user was active

``title``
	The person's company title

``presence``
	A ``dict`` of the values:
	
	``status``
		A status message, or ``None``

	``idle``
		The number of seconds the user has been idle, or ``None``

	``show``
		The status category, one of: ``'away'``, ``'chat'``, ``'dnd'``, ``'xa'``, or ``None``

	``is_online``
		``True`` if the user is online

``created``
	When the User was created

``mention_name``
	User's @mention name

``is_group_admin``
	``True`` if the user is an admin of the group/company/etc

``timezone``
	The user's timezone

``email``
	The user's email

``photo_url``
	The user's URL as a string.

Emoticons Collection
--------------------
Defines nothing above `All Collections`_

Emoticon
--------

Fields
~~~~~~
``shortcut``
	(Stubbed) The name used to invoke the emoticon, as in "(shortcut)"

``url``
	(Stubbed) The image file for this emoticon

``creator``
	The User_ that created this emoticon

``width``
	The width of the image, in pixels

``height``
	The height of the image, in pixels

``audio_path``
	(Optional) An audio file that should be played at the same time