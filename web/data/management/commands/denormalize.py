"""
Thin wrapper around managers.denormalize
"""

import django
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.contenttypes.models import ContentType

from data.models import Recipient, Payment, Scheme, FishData

class Command(NoArgsCommand):
    
    def recipient(self):
        for row in FishData.denormalize.recipient():
            try:
                v = Recipient.objects.get(cfr=row.cfr)
            except:
                v = Recipient()
            # print dir(row)
            v.pk = row.cfr
            v.name = row.vessel_name
            v.amount = row.amount or 0
            v.country = row.iso_country
            v.port = row.port_name or ''
            v.save()

    def schemes(self):
        years = [year.year for year in FishData.denormalize.years()]
        years.append(None)
        for year in years:
            for scheme in FishData.denormalize.schemes(year):
                try:
                    s = Scheme.objects.get(scheme_id=scheme.scheme_id, year=scheme.year)
                except Exception, e:
                    s = Scheme()
                s.scheme_id = scheme.scheme_id
                s.name = scheme.name
                s.year = scheme.year
                s.total = scheme.total or 0
                s.traffic_light = scheme.traffic_light
                s.save()
        
    
    def payments(self):
        for row in FishData.denormalize.payments():
            try:
                v = Recipient.objects.get(recipient_id=row.cfr)
                s = Scheme.objects.get(year=row.year, scheme_id=row.scheme2_id)
                try:
                    p = Payment.objects.get(payment_id=row.id,)
                except:
                    p = Payment(recipient_id=v, payment_id=row.id,)
                row_dict = row.__dict__
                row_dict['port'] = row_dict.get('port') or ''

                p.amount = row_dict['total_subsidy'] or 0
                p.year = row_dict['year']
                p.country = row_dict['iso_country']
                p.scheme = s
                p.save()
            except Exception, e:
                print e
                print row_dict
                print "no vessel"
    
    def handle_noargs(self, **options):
        print "payments"
        self.payments()
        # print "recipient"
        # self.recipient()
        # print "schemes"
        # self.schemes()
