#botcoin

Twitter-driven (OAuth) RSS feed generator written in GoogleAppScript, based on JavaScript, that uses event-driven networking engine Twisted to execute simple `LoopingCall` commands into IRC channels.

##Authentication

You auth through Twitter's OAuth, http://dev.twitter.com, configured
at ``./src/twitter.search.feed.coffee``.

##Why?

I wanted to spam a chatroom.

The key here is that the GA Script accepts a CGI parameter (q). It can be fed
any arbitrary string, like a member list of a chan or a recording of a chan.

##What Twitter knows

You can even collect all the RSS feeds Twitter can think of based on a syntatic
analysis of your codebase. Use reserved like "controller" or "event" often?

Then visualize your codebase as a region of tags in Twitter.

##Twisted

    @TODO Read channel content
          Feed to GAS
          Loop over terms
          Timing term collection

##Ideas

https://github.com/OmerShapira/Syntactic allows for lexical categorization. Do
I use Twitter as the Control? Or IRC chans?

I'm sure the sizes of lexical groups will tell us something about intelligence
across Internet denizen subspaces.

###Applications

1. Discover youth ranges, distribute LGBT youtube video links.
