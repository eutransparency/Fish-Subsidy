import csv
import sys

import django
from django.core.management.base import BaseCommand
from django.utils import translation

from data.models import EffData

class SKV(csv.excel):
    # like excel, but uses semicolons
    delimiter = ";"

csv.register_dialect("SKV", SKV)


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        f = csv.DictReader(open('../data/website20120807.txt', 'r'), dialect='SKV')
        EffData.objects.all().delete()
        for line in f:
            if not line['yearAllocated']:
                del line['yearAllocated']
            else:
                try:
                    int(line.get('yearAllocated'))
                except ValueError:
                    del line['yearAllocated']
                
            if not line['yearPaid']:
                del line['yearPaid']
            else:
                try:
                    int(line['yearPaid'])
                except ValueError:
                    del line['yearPaid']
                
            try:
                E = EffData()
                floats = ('amountEuAllocatedEuro', 
                          'amountEuPaymentEuro', 
                          'amountTotalAllocatedEuro', 
                          'amountTotalPaymentEuro')
                for f in floats:
                    line[f] = float(line[f] or 0)
                
                E.__dict__.update(line)
                E.save()
            except:
                print line
                raise