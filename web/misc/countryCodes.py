import sys
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

def country_codes(code=None):
  countries = SortedDict()
  countries['EU'] = _('All Countries' )

  countries['AT'] = _('Austria')            
  countries['BE'] = _('Belgium')            
  countries['BG'] = _('Bulgaria')           
  countries['CY'] = _('Cyprus')             
  countries['CZ'] = _('Czech Republic')     
  countries['DK'] = _('Denmark')            
  countries['EE'] = _('Estonia')            
  countries['FI'] = _('Finland')            
  countries['FR'] = _('France')             
  countries['DE'] = _('Germany')            
  countries['GR'] = _('Greece')             
  countries['HU'] = _('Hungary')            
  countries['IE'] = _('Ireland')            
  countries['IT'] = _('Italy')              
  countries['LV'] = _('Latvia' )            
  countries['LT'] = _('Lithuania')          
  countries['LU'] = _('Luxembourg')         
  countries['MT'] = _('Malta')              
  countries['NL'] = _('Netherlands')        
  countries['PL'] = _('Poland')             
  countries['PT'] = _('Portugal')           
  countries['RO'] = _('Romania')            
  countries['SK'] = _('Slovakia')           
  countries['SI'] = _('Slovenia')           
  countries['ES'] = _('Spain')              
  countries['SE'] = _('Sweden')             
  countries['GB'] = _('United Kingdom')     
  
  if code:
    if code in countries.keys():
      return {'code' : code, 'name' : countries[code]}
    else:
      raise ValueError, "%s not a country" % code
  else:
    return countries.keys()

if __name__ == "__main__":
  print country_codes()