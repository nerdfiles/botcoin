# ./scrape.coffee
# @see http://www.labnol.org/?p=27931
#
# This is a rendition in CoffeeScript. Compile it to JS, deploy it from Google
# Drive.
#
# @nerdfiles
Scraper.start 'CONSUMER_KEY', 'CONSUMER_SECRET'

class Scraper

  # Get your Twitter keys from dev.twitter.com
  @start: (key, secret) ->

    @initialize()

  @initialize: ( key, secret ) ->

    ScriptProperties.setProperty 'TWITTER_CONSUMER_KEY', key
    ScriptProperties.setProperty 'TWITTER_CONSUMER_SECRET', secret

    url = ScriptApp.getService().getUrl()

    if url
      @connectTwitter()
    MailApp.sendEmail Session.
      getActiveUser().
      getEmail(), 'Twitter RSS Feeds', msg

  @JSONtoRSS: (json, type, key) ->

    @oAuth()

    options:
      'method': 'get',
      'oAuthServiceName':'twitter',
      'oAuthUseToken':'always'

    try

      result = UrlFetchApp.fetch json, options

      if result.getResponseCode() == 200

        tweets = Utilities.jsonParse result.getContentText()

        if type == 'search'
          tweets = tweets.statuses

        if tweets

          len = tweets.length
          rss = ''

          if (len)

            rss  = '<?xml version=\'1.0\'?><rss version=\'2.0\'>'
            rss += ' <channel><title>Twitter ' + type + ': ' + key + '</title>'
            rss += ' <link>' + @htmlentities (json) + '</link>'
            rss += ' <pubDate>' + new Date() + '</pubDate>'
            for i in [0..len] by 1
              sender = tweets[i].user.screen_name
              tweet  = @htmlentities tweets[i].text
              rss += '<item><title>' + sender + ': ' + tweet + '</title>'
              rss += ' <author>' + tweets[i].user.name + ' (@' + sender +
                ')</author>'
              rss += ' <pubDate>' + tweets[i].created_at + '</pubDate>'
              rss += ' <guid isPermaLink=\'false\'>' + tweets[i].id_str +
                '</guid>'
              rss += ' <link>https://twitter.com/' + sender + '/statuses/' +
                tweets[i].id_str + '</link>'
              rss += ' <description>' + tweet + '</description>'
              rss += '</item>'
            rss += '</channel></rss>'

            rss

    catch: (e) ->

      Logger.loge.toString()

  @connectTwitter: () ->

    @oAuth()

    search = 'https://api.twitter.com/1.1/application/rate_limit_status.json'

    options:
      'method': 'get'
      'oAuthServiceName':'twitter'
      'oAuthUseToken':'always'

    try:

      result = UrlFetchApp.fetch search, options

    catch: (e) ->

      Logger.log e.toString()


  @htmlentities: (str) ->

    str = str.replace /&/g, '&amp;'
    str = str.replace />/g, '&gt;'
    str = str.replace /</g, '&lt;'
    str = str.replace /'/g, '&quot;'
    str = str.replace /'/g, '&#039;'
    str

  @oAuth: () ->

    oauthConfig = UrlFetchApp.addOAuthService 'twitter'
    oauthConfig.setAccessTokenUrl 'https://api.twitter.com/oauth/access_token'
    oauthConfig.setRequestTokenUrl 'https://api.twitter.com/oauth/request_token'
    oauthConfig.setAuthorizationUrl 'https://api.twitter.com/oauth/authorize'
    oauthConfig.setConsumerKey ScriptProperties.
      getProperty 'TWITTER_CONSUMER_KEY'
    oauthConfig.setConsumerSecret ScriptProperties.
      getProperty 'TWITTER_CONSUMER_SECRET'
