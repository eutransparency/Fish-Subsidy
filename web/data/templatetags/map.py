from django.template import Library, Node
register = Library()

import settings

def get_map(port):
    if port.port_lng and port.port_lat:
        lat = port.port_lat
        lon = port.port_lng
        t = float(lat) + 0.03
        b = float(lat) - 0.03
        r = float(lon) + 0.03
        l = float(lon) - 0.03
    else:
        fail = True
    api_key = settings.GOOGLE_MAPS_API_KEY
    return locals()
register.inclusion_tag('blocks/map.html')(get_map)
