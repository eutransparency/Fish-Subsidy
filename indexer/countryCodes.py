import sys

def country_codes(code=None, local='GB'):
  countries = {
  'AT'	:	{
    'GB' : 'Austria'
    },
  'BE'	:	{
    'GB' : 'Belgium'
    },
  'BG'	:	{
    'GB' : 'Bulgaria'
    },
  'CZ'	:	{
    'GB' : 'Czech'
    },
  'DK'	:	{
    'GB' : 'Denmark'
    },
  'EE'	:	{
    'GB' : 'Estonia'
    },
  'FI'	:	{
    'GB' : 'Finland'
    },
  'FR'	:	{
    'GB' : 'France'
    },
  'DE'	:	{
    'GB' : 'Germany'
    },
  'GR'	:	{
    'GB' : 'Greece'
    },
  'HU'	:	{
    'GB' : 'Hungary'
    },
  'IE'	:	{
    'GB' : 'Ireland'
    },
  'IT'	:	{
    'GB' : 'Italy'
    },
  'LV'	:	{
    'GB' : 'Latvia'
    },
  'LT'	:	{
    'GB' : 'Lithuania'
    },
  'LU'	:	{
    'GB' : 'Luxembourg'
    },
  'NL'	:	{
    'GB' : 'Netherland'
    },
  'PL'	:	{
    'GB' : 'Poland'
    },
  'PT'	:	{
    'GB' : 'Portugal'
    },
  'SK'	:	{
    'GB' : 'Slovakia'
    },
  'SI'	:	{
    'GB' : 'Slovenia'
    },
  'ES'	:	{
    'GB' : 'Spain'
    },
  'SE'	:	{
    'GB' : 'Sweden'
    },
  'GB'	:	{
    'GB' : 'United Kingdom'
    },
  }
  
  if code:
    if code in countries.keys():
      return {'code' : code, 'name' : countries[code][local]}
    else:
      raise ValueError, "%s not a country" % code
  else:
    return countries.keys()

if __name__ == "__main__":
  print country_codes()