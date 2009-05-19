from fishsubsidy.indexer import countryCodes

def country(request):
    from django.conf import settings
    countryCode = request.META['PATH_INFO'].split('/')[1]
    
    try:
      country = countryCodes.country_codes(countryCode)
    except ValueError:
      country = {'code' : ''}
    
    return {'country': country}
