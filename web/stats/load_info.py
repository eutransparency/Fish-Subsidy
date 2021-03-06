import csv
import re
import codecs
from django.conf import settings
from django.contrib.humanize.templatetags import humanize
from django.utils.translation import ugettext_lazy as _


def load_info(country=None, format=True, year=settings.DEFAULT_YEAR, locale=settings.LANGUAGE_CODE):
  filepath = "%s/stats_%s.csv" % (settings.STATS_PATH, locale)
  stats = csv.DictReader(codecs.open(filepath, "U"))
  if country:
    for row in stats:
      if row['Country'] == country:
        info = row
        if format:

          top_5 = range(5)
          
          # Format elements
          for k,v in info.items():
            try:
              if k.startswith('Top 5'):
                i,j = v.split('=')
                top_5[int(k[-4:-3])-1] = (i,humanize.intcomma(j))
                del info[k]

              info[k] = humanize.intcomma(info[k])
              formatter = k[-2:]
              # print formatter
              if formatter == " E":
                # new_k = re.sub(' \(.*\).*', '',k)
                new_k = k[:-2].strip()
                info[new_k] = u"&euro;%s" % info[k]
                del info[k]
              if formatter == "ET":
                # new_k = re.sub(' \(.*\).*', '',k)
                new_k = k[:-2].strip()
                info[new_k] = _(u"&euro;%(number)s,000") % {'number' : info[k]}
                del info[k]
              if formatter == "EM":
                new_k = re.sub(' \(.*\).*', '',k)
                new_k = new_k.strip()
                info[new_k] = _(u"&euro;%(number)s Million") % {'number' : info[k]}
                del info[k]
              if formatter == " %":
                new_k = re.sub(' \(.*\).*', '',k)
                new_k = new_k.strip()
                info[new_k] = u"%s%%" % info[k]
                del info[k]
              if formatter == " T":
                # new_k = re.sub(' \(.*\).*', '',k)
                new_k = k[:-2].strip()
                info[new_k] = _(u"%(number)s Tonnes") % {'number' : info[k]}
                del info[k]
              else:
                new_k = re.sub(' \(.*\).*', '',k)
                new_k = new_k.strip()
                info[new_k] = u"%s" % info[k]
                del info[k]
                
                

            except Exception,e:
              pass

          info['top_5'] = top_5
          for key, value in info.items():
            del info[key]
            key = re.sub(" ", "_", key.lower())
            key = re.sub("-", "_", key.lower())
            key = re.sub("\(|\)", "_", key.lower())
            key = re.sub("%", "", key)
            info[key] = value
        

        return info
  else:
    return stats

if __name__ == "__main__":
  a = load_info('GB')
  for b in a.items():
    # pass
    print b