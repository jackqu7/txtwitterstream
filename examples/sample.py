#!/usr/bin/env python
# coding: utf-8

import twitterstream
from twisted.internet import reactor

class consumer(twitterstream.TweetReceiver):
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
    TwistedTwitterStream.sample("username", "password", consumer())
    reactor.run()
