from django.template import Library
import urllib
register = Library()

@register.simple_tag
def parse_qs(qs, k=None,v=None):
    qs = qs.copy()
    get_dict = {}

    get_dict[k] = unicode(v).encode('utf8')

    for old_k, old_v in qs.items():
        if k != old_k:
            get_dict[old_k] = unicode(old_v).encode('utf8')
        # print qs[k]


    # Normally, we don't want to keep the page element of the string
    if 'page' in qs:
        del qs['page']
    return "?%s" % urllib.urlencode(get_dict)

@register.simple_tag
def parse_sort_qs(qs, k=None, v=None):
    qs = qs.copy()
    get_dict = {}
    for old_k,old_v in qs.items():
        get_dict[old_k] = unicode(old_v).encode('utf8')

    old_v = qs.get(k, "")
    if k:
        if v in [old_v, old_v[1:]]:
            # We're updating the same key, and just reversing the order
            if old_v.startswith('-'):
                v = old_v[1:]
            else:
                v = "-%s" % old_v
        # else:
    get_dict[k] = v

    # Normally, we don't want to keep the page element of the string
    if 'page' in get_dict:
        del get_dict['page']
    return "?%s" % urllib.urlencode(get_dict)







