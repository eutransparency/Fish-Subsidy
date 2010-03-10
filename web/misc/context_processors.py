from datetime import datetime
import settings
from django.core.cache import cache
import twitter

def latest_tweet(request):
    tweet = cache.get( 'tweet' )

    if tweet:
        return {"tweet": tweet}
    try:
        tweet = twitter.Api().GetUserTimeline(settings.TWITTER_USER)[0]
        tweet.date = datetime.strptime( tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y" )
        cache.set( 'tweet', tweet, settings.TWITTER_TIMEOUT )
    except:
        tweet = {}
    return {"tweet": tweet}