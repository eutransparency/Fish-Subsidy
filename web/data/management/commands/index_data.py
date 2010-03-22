import django
from django.core.management.base import NoArgsCommand, CommandError
from data.models import Vessel, FishData
import csv
import codecs

class Command(NoArgsCommand):

  def handle_noargs(self, **options):
    class SKV(csv.excel):
        # like excel, but uses semicolons
        delimiter = ";"

    csv.register_dialect("SKV", SKV)
    
    f = codecs.open('../data/fish.csv', 'r')
    items = csv.DictReader(f, delimiter=";")
    for item in items:
      obj = FishData()
      # if item.get('id'):
        # print "deleted"
        # del item['id']
      if item.get('year'):
        if item['year'] == "":
          print "break"
      # print "\n".join(item.keys())
      # print item['total cost']
      if item.get('cfr'):
        print item['cfr']
      obj.__dict__.update(item)
      try:
        obj.save()
      except Exception, e:
        print e
        # print repr(item['year'])
        # print item
        # print item['id']
        # break
        pass