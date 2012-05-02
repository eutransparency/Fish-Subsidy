from django.core.cache import cache

import settings
from models import Feature

def featured_items(request):

    in_features = bool(request.META['PATH_INFO'].split('/')[1] =='features')
    
    features = {}
    
    if in_features:
        features['featured_items'] = cache.get('featured_items')
        
        if not features['featured_items']:
            features['featured_items'] = Feature.objects.filter(featured=True, published=True,).order_by('-pk')
            cache.set('featured_items', featured_items)
        else:
            return {'featured_items' : featured_items}
    else:
        return {}
        
    