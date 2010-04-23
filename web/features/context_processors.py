from django.core.cache import cache

import settings
from models import Feature

def featured_items(request):
    lan = request.locale.language
    featured_items = cache.get('featured_items_%s' % lan)
    
    in_features = bool(request.META['PATH_INFO'].split('/')[1] =='features')
    
    if not featured_items:
        featured_items = Feature.objects.filter(featured=True, published=True,).for_language(lan)[:3]
        cache.set('featured_items_%s' % lan, featured_items)
    if featured_items and not in_features:
        return {'featured_items' : featured_items}
    else:
        return {}