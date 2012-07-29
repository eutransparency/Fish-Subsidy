from datetime import datetime
import settings
from django.core.cache import cache
from utils import get_tweets

def latest_tweets(request):
    tweets = cache.get( 'tweets' )
    tweets = None

    if tweets:
        return {"tweets": tweets}
    try:
        tweets = get_tweets()
    except:
        tweets = []
    return {"tweets": tweets}
