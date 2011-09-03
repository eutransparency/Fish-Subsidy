import django
from django.core.management.base import NoArgsCommand, CommandError
from data.models import Scheme
import csv
import codecs
from django.conf import settings

class Command(NoArgsCommand):

  def handle_noargs(self, **options):
    
    for l in settings.LANGUAGES:
        try:    
            f = codecs.open('../data/scheme_names_%s.csv' % l[0], 'r')
            items = csv.DictReader(f, dialect='excel')
            for item in items:
                try:
                    s = Scheme.objects.get(pk=item['id'])
                    s.__dict__['name_%s'% l[0]]  = item['name']
                    s.save()
                except Exception, e:
                    print e
        except:
            print l