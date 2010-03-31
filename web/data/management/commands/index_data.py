import django
from django.core.management.base import NoArgsCommand, CommandError
from data.models import Recipient, FishData
import csv
import codecs

class Command(NoArgsCommand):

  def handle_noargs(self, **options):
    # class EXCEL(csv.excel):
    #     # like excel, but uses semicolons
    #     delimiter = ","
    # 
    # csv.register_dialect("EXCEL", EXCEL)
    
    f = codecs.open('../data/fish.csv', 'r')
    items = csv.DictReader(f, dialect='excel')
    for item in items:
        for k,v in item.items():
            if v == '':
                item[k] = None
            # if v:
            #     try:
            # 
            #         if new_k == "geo2":
            #           if len(v) != len(v_decode):
            #               item[k] = v_decode
            #     except Exception, e:
            #         print e
            #         pass
            # if v == '':
            #     item[new_k] = None
        removed_fields = [
            'id',
            'domain',
            'perp_length',
            'measure',
            'provisional_fifg',
            'your_id',
            'provisional_total_cost',
            'commune',
            'indicator',
            'flag',
            'grt_tonnage',
            'country',
            'action',
            'port_code',
            'quantity',
            'provisional fifg',
            'approval date',
            'provisional total cost',
        ]
        for field in removed_fields:
            if field in item:
                del item[field]
        try:
            
            FishData.objects.get_or_create(**item)
            # d.save()
        except Exception, e:
            # for k,v in item.items():
            #     print k,repr(v)
            print e
            # print repr(item)

            
            # break