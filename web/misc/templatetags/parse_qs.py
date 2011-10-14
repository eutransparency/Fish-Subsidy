from django.template import Library
import urllib
register = Library()

@register.simple_tag
def parse_qs(qs, k=None,v=None):
    qs = qs.copy()
    for k,v in qs.items():
        qs[k] = unicode(v).encode('utf8')
    if k:
        qs[k] = unicode(v).encode('utf8')
    # Normally, we don't want to keep the page element of the string
    if 'page' in qs:
        del qs['page']
    return "?%s" % urllib.urlencode(dict(qs))

@register.simple_tag
def parse_sort_qs(qs, k=None, v=None):
    qs = qs.copy()
    for k,v in qs.items():
        qs[k] = unicode(v).encode('utf8')

    old_v = qs.get(k, "")
    if k:
        if v in [old_v, old_v[1:]]:
            # We're updating the same key, and just reversing the order
            if old_v.startswith('-'):
                v = old_v[1:]
            else:
                v = "-%s" % old_v

        qs[k] = v


    # Normally, we don't want to keep the page element of the string
    if 'page' in qs:
        del qs['page']
    return "?%s" % urllib.urlencode(dict(qs))

