from twisted.words.protocols import irc
from twisted.internet.task import LoopingCall
from twisted.internet import reactor, protocol

from twitter import *

import feedparser

# consumer_key = "XpaitKsl1dAYbYTGCkw"
# consumer_secret = "4m9QVS2HubbccRskIY2C1iufwBxVEBeIHXYixwLmRMo"
# access_key = "286402780-0oXOIaYC4B7ypQWE84Z0dCoXnaN1QZB9aocFzzG0"
# access_secret = "u1W0FmSPBO4AC8tvzuHG9W3QWGSMgIeE6QBYFvN6Jli6Z"

# https://github.com/sixohsix/twitter/blob/master/twitter/oauth.py#L78
auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)

# https://github.com/sixohsix/twitter/blob/master/twitter/api.py#L241
t = Twitter(auth=auth)

user = "market"  # @market, essentially.
Channel = "irc.freenode.com"  # Market context.


class Bot(irc.IRCClient):

    def __init__(self):
        self.nickname = "FreeBTC"  # irc nick
        # self.channel = "##freebtc"  # irc channel (TODO: self.channel = [])
        self.channel = "##ventures"  # irc channel (TODO: self.channel = [])
        self.oldresults = ""
        self.callCounter = 0

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print "DISCONNECTED for " + reason

    def signedOn(self):
        self.join(self.channel)

    def joined(self, channel):
        print "JOINED " + channel
        lc = LoopingCall(self.checkRSS)
        lc.start(70)

    def privmsg(self, user, channel, msg):
        user = user.split("!", 1)[0]

        if channel == self.nickname:
            print user + " says: " + msg
            return

        if msg.startswith(self.nickname + ":"):
            print user + " says: " + msg
            return

    def checkRSS(self):
        '''
            Host scraper on Google Drive. Deploy it.

            @see http://www.labnol.org/?p=27931
            @nerdfiles
        '''
        feed = feedparser.parse(
            'https://script.google.com/macros/s/AKfycbwk-KM8gW-QDNTapXRNzQqqjHR_sa9cS12fPkGzxPW6Q4LWGmSb/exec?action=search&q=freebtc')
        self.results = feed['entries'][self.callCounter]['title']
        self.callCounter = self.callCounter + 1

        if self.oldresults != "":
            if self.oldresults != "" and self.oldresults != self.results:
                msg = self.results.encode("ascii", "ignore")
                err = self.prepMessage(msg)
                if err != "error":
                    self.sendMessage(msg)

        else:
            msg = self.results.encode("ascii", "ignore")
            err = self.prepMessage(msg)
            if err != "error":
                self.sendMessage(msg)

        self.oldresults = self.results

    def prepMessage(self, msg):
        msg = msg.replace("\r", "").replace("\n", "")
        if msg.find("free"):
            return msg
        else:
            return "error"

    def sendMessage(self, msg):
        print(msg)
        # before you sendMessage, be sure to prepMessage(msg)
        # TODO: have prepMessage here, instead of seperate function
        self.sendLine("PRIVMSG %s :%s" % (self.channel, msg))


class BotFactory(protocol.ClientFactory):

    def __init__(self):
        self.channel = "##ventures"

    def buildProtocol(self, addr):
        p = Bot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

if __name__ == "__main__":
    f = BotFactory()
    reactor.connectTCP(Channel, 6667, f)
    reactor.run()