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
        
        # you may call self.disconnect() anytime to
        # permanently disconnect from the Twitter Stream

if __name__ == "__main__":
    twitterstream.Client("username", "password").filter(consumer(),
            locations="-122.75,36.8,-121.75,37.8,-74,40,-73,41")
    reactor.run()
