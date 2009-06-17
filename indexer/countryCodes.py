import sys
from django.utils.datastructures import SortedDict


def country_codes(code=None, local='GB'):
  countries = SortedDict()
  countries['BE'] = {'GB' : 'Belgium'}
  countries['BG']	=	{'GB' : 'Bulgaria'}
  countries['CZ']	=	{'GB' : 'Czech Republic'}
  countries['DK']	=	{'GB' : 'Denmark'}
  countries['DE']	=	{'GB' : 'Germany'}
  countries['EE']	=	{'GB' : 'Estonia'}
  countries['IE']	=	{'GB' : 'Ireland'}
  countries['GR']	=	{'GB' : 'Greece'}
  countries['ES']	=	{'GB' : 'Spain'}
  countries['FR']	=	{'GB' : 'France'}
  countries['IT']	=	{'GB' : 'Italy'}
  countries['CY']	=	{'GB' : 'Cyprus'}
  countries['LV']	=	{'GB' : 'Latvia'}  
  countries['LT']	=	{'GB' : 'Lithuania'}
  countries['LU']	=	{'GB' : 'Luxembourg'}
  countries['HU']	=	{'GB' : 'Hungary'}
  countries['MT']	=	{'GB' : 'Malta'}
  countries['NL']	=	{'GB' : 'Netherlands'}
  countries['AT']	=	{'GB' : 'Austria'}
  countries['PL']	=	{'GB' : 'Poland'}
  countries['PT']	=	{'GB' : 'Portugal'}
  countries['RO']	=	{'GB' : 'Romania'}
  countries['SI']	=	{'GB' : 'Slovenia'}
  countries['SK']	=	{'GB' : 'Slovakia'}  
  countries['FI']	=	{'GB' : 'Finland'}
  countries['SE']	=	{'GB' : 'Sweden'}
  countries['GB']	=	{'GB' : 'United Kingdom'}
  
  
  if code:
    if code in countries.keys():
      return {'code' : code, 'name' : countries[code][local]}
    else:
      raise ValueError, "%s not a country" % code
  else:
    return countries.keys()

if __name__ == "__main__":
  print country_codes()