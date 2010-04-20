====================
TwistedTwitterStream
====================
:Info: See `Twitter Streaming API <http://apiwiki.twitter.com/Streaming-API-Documentation>`_ for more information. See `github <http://github.com/fiorix/twisted-twitter-stream/>`_ for the latest source.
:Author: Wade Simmons <wade@wades.im> and Alexandre Fiori <fiorix@gmail.com>

About
=====
The ``TwistedTwitterStream`` package provides an event-driven API for receiving `Twitter <http://twitter.com>`_ status updates through the asynchronous `Twitter Streaming API <http://apiwiki.twitter.com/Streaming-API-Documentation>`_.

The following methods are supported:
 - `firehose <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/firehose>`_
 - `retweet <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/retweet>`_
 - `sample <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/sample>`_
 - `filter <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/filter>`_

Notes
=====
 - A JSON parser is required. Like `json <http://docs.python.org/library/json.html>`_, `simplejson <http://pypi.python.org/pypi/simplejson/>`_, or `jsonutil <http://tahoe-lafs.org/trac/pyutil/browser/pyutil/pyutil/jsonutil.py>`.
 - All methods will automatically reconnect to the server with an exponential back-off. See `t.i.p.ReconnectingClientFactory <http://twistedmatrix.com/documents/8.2.0/api/twisted.internet.protocol.ReconnectingClientFactory.html>`_ for details.
 - All methods must be initialized with a *consumer* object, inherited from `TwistedTwitterStream.TweetReceiver`
 - No proxy support.

Examples
========
Examples are available in the *examples/* directory.

Credits
=======
Thanks to (in no particular order):

- Arnaldo Moraes
  
  - Testing, patching and using for private projects

- Vanderson Mota

  - Patching setup.py and PyPi maintenance

Licence
=======
Permission is hereby granted to any person obtaining a copy of this work to
deal in this work without restriction (including the rights to use, modify,
distribute, sublicense, and/or sell copies).
