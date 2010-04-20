#!/usr/bin/env python
# coding: utf-8
#
# follow is a list of user IDs, not screen names
# use something like this to get user IDs:
#
#    screen_name = "BarackObama"
#    fd = urllib.urlopen("http://twitter.com/users/show/%s.json" % screen_name)
#    doc = json.loads(fd.read())
#    fd.close()
#    print doc.get("id")

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
    txtwitterstream.Client("username", "password").filter(consumer(),
            follow=["101010", "202020", "303030", "404040"])
    reactor.run()
