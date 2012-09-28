import django
from django.core.management.base import NoArgsCommand, CommandError
from data.models import Port, FishData
import csv
import codecs
from django.conf import settings

class Command(NoArgsCommand):

  def handle_noargs(self, **options):
    
    for p in Port.objects.all():
        try:
            po = FishData.objects.filter(port_name=p.name, iso_country=p.country)[0]
            p.lat = po.port_lat
            p.lng = po.port_lng
            p.save()
        except IndexError:
            pass