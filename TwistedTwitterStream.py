# coding: utf-8
#
# Copyright 2009 Alexandre Fiori
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

__author__ = "Alexandre Fiori"
__version__ = "0.0.2"

"""Twisted client library for the Twitter Streaming API:
http://apiwiki.twitter.com/Streaming-API-Documentation"""

import base64
import urllib

from zope.interface import implements
from twisted.protocols import basic
from twisted.internet import defer, succeed, reactor, protocol
from twisted.web import client
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer

from twisted.web.client import ResponseDone
from twisted.web.http import PotentialDataLoss

try:
    import simplejson as _json
except ImportError:
    try:
        import json as _json
    except ImportError:
        raise RuntimeError("A JSON parser is required, e.g., simplejson at "
                           "http://pypi.python.org/pypi/simplejson/")


class TweetReceiver(object):
    def connectionMade(self):
        pass

    def connectionFailed(self, why):
        pass

    def tweetReceived(self, tweet):
        raise NotImplementedError

    def _registerProtocol(self, protocol):
        self._streamProtocol = protocol

    def disconnect(self):
        if hasattr(self, "_streamProtocol"):
            self._streamProtocol.factory.continueTrying = 0
            self._streamProtocol.transport.loseConnection()
        else:
            raise RuntimeError("not connected")

class _StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class _TwitterStreamProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.consumer = factory.consumer

    def lineReceived(self, line):
        line = line.strip()
        if line:
            tweet = _json.loads(line)
            self.consumer.tweetReceived(tweet)
            
    def connectionLost(self, reason):
        if reason.check(ResponseDone) or reason.check(PotentialDataLoss):
            pass
        else:
            print "connection lost: %s" % reason

class _HTTPReconnectingClientFactory(protocol.ReconnectingClientFactory):
    maxDelay = 120
    protocol = client.HTTP11ClientProtocol
    
    def __init__(self, method, path, headers, consumer, body=None):
        self.method = method
        self.path = path
        self.headers = headers
        self.consumer = consumer
        self.proto = None
        self.body = body
    
    def buildProtocol(self, addr):
        self.resetDelay()
        proto = self.protocol()
        proto.factory = self
        reactor.callLater(0, self.connected, proto)
        self.proto = proto
        return proto
        
    def force_reconnect(self):
        self.proto.transport.loseConnection()
    
    def connected(self, proto):
        d = proto.request(client.Request(self.method, self.path, self.headers, (self.body and _StringProducer(self.body))))
        d.addCallback(self._got_headers, self.consumer)
        d.addErrback(defer.logError)
    
    def _got_headers(self, response, consumer):
        if response.code == 200:
            response.deliverBody(_TwitterStreamProtocol(consumer))
            consumer.connectionMade()
        else:
            consumer.connectionFailed(Exception("Twitter returned: %s %s" % (response.code, response.phrase)))
            self.continueTrying = 0
            if self.proto.transport:
                self.proto.transport.loseConnection()
 
def _get_headers(username, password):
    headers = Headers()
    headers.addRawHeader("Authorization", _auth_header(username, password))
    headers.addRawHeader("Host", "stream.twitter.com")
    return headers

def _auth_header(username, password):
    return "Basic %s" % base64.encodestring("%s:%s" % (username, password)).strip()

def _stream(username, password, consumer, endpoint, post_body=None):
    f = _HTTPReconnectingClientFactory("GET", "/1/statuses/firehose.json", _get_headers(username, password), consumer)
    reactor.connectTCP("stream.twitter.com", 80, f)

def firehose(username, password, consumer):
    _stream(username, password, consumer, "/1/statuses/firehose.json")

def retweet(username, password, consumer):
    _stream(username, password, consumer, "/1/statuses/retweet.json")

def sample(username, password, consumer):
    _stream(username, password, consumer, "/1/statuses/sample.json")

def filter(username, password, consumer, count=0, delimited=0, track=[], follow=[]):
    qs = []
    if count:
        qs.append("count=%s" % urllib.quote(count))
    if delimited:
        qs.append("delimited=%d" % delimited)
    if follow:
        qs.append("follow=%s" % ",".join(follow))
    if track:
        qs.append("track=%s" % ",".join([urllib.quote(s) for s in track]))

    if not (track or follow):
        raise RuntimeError("At least one parameter is required: track or follow")
    
    _stream(username, password, consumer, "/1/statuses/filter.json", "&".join(qs))