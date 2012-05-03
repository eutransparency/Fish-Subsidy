from django.core.cache import cache

import settings
from models import Feature

def featured_items(request):

    in_features = bool(request.META['PATH_INFO'].split('/')[1] =='features')
    
    features = {}
    
    if in_features:
        # Don't show context features on features page!
        return {}

    features['featured_items'] = cache.get('featured_items')
        
    if not features['featured_items']:
        features['featured_items'] = Feature.objects.filter(featured=True, published=True,).order_by('-pk')
        cache.set('featured_items', features['featured_items'])

    return {'featured_items' : features['featured_items']}

        
    