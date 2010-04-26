import django
from django.core.management.base import NoArgsCommand, CommandError
from data.models import Scheme
import csv
import codecs

class Command(NoArgsCommand):

  def handle_noargs(self, **options):
    
    f = codecs.open('../data/scheme_names_es.csv', 'r')
    items = csv.DictReader(f, dialect='excel')
    for item in items:
        try:
            s = Scheme.objects.get(pk=item['id'])
            s.name_es = item['name']
            s.save()
        except Exception, e:
            print e
