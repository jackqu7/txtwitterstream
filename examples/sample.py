#!/usr/bin/env python
# coding: utf-8

import txtwitterstream
from twisted.internet import reactor

class consumer(txtwitterstream.TweetReceiver):
    def connectionMade(self):
        print "connected..."

    def connectionFailed(self, why):
        print "cannot connect:", why
        reactor.stop()

    def tweetReceived(self, tweet):
        print "new tweet:", repr(tweet)

if __name__ == "__main__":
    #TwistedTwitterStream.firehose("username", "password", consumer())
    #TwistedTwitterStream.retweet("username", "password", consumer())
    txtwitterstream.Client("username", "password").sample(consumer())
    reactor.run()
