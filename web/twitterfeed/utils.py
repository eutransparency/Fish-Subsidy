import urllib2
import urllib
import json
import time
import datetime
from django.conf import settings
from django.core.cache import cache
from tweet_text_parser import TweetTextParser

def get_tweets(limit=10, username=settings.TWITTER_USER):
    print limit
    tweets = cache.get('tweets')
    if not tweets:
        base_url = "https://api.twitter.com/1/statuses/user_timeline.json"
        prams = {
            'include_entities' : 'true',
            'include_rts' : 'true',
            'screen_name' : username,
            'count' : limit,
            # 'trim_user' : 'true',
            'exclude_replies' : 'true',
        }
        url = "%s?%s" % (base_url, urllib.urlencode(prams))
        try:
            res = urllib2.urlopen(url)
            tweets = json.loads(res.read())
            for tweet in tweets:
                struct = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                tweet['created_at'] =  datetime.datetime.fromtimestamp(time.mktime(struct))
            t = TweetTextParser(tweets)
            tweets = t.parse_all()
        except urllib2.URLError:
            tweets = []
        cache.set('tweets', tweets, settings.TWITTER_TIMEOUT)
    return tweets
    