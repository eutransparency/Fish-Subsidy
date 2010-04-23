"""
Thin wrapper around managers.denormalize
"""

import django
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.contenttypes.models import ContentType

from data.models import Recipient, Payment, Scheme, Port, FishData

class Command(NoArgsCommand):

    def ports(self):

        for port in FishData.denormalize.ports():
            try:
                p = Port.objects.get(name=port.port_name, geo1=port.geo1)
            except Exception, e:
                p = Port()

            p.name = port.port_name
            p.country = port.iso_country
            p.total = port.total or 0
            p.geo1 = port.geo1
            p.geo2 = port.geo2
            p.save()

    def recipient(self):
        for row in FishData.denormalize.recipient():
            recipient_id = row.recipient_id_fixed
            if recipient_id:
                try:
                    v = Recipient.objects.get(recipient_id=recipient_id)
                except:
                    v = Recipient()
                try:
                    p = Port.objects.get(name=row.port_name)
                except Exception, e:
                    p = None

                if row.cfr:
                    v.recipient_type = "vessel"
                else:
                    v.recipient_type = "nonvessel"
                v.pk = recipient_id
                v.name = row.vessel_name
                v.amount = row.amount or 0
                v.country = row.iso_country
                if p: v.port = p
                v.geo1 = row.geo1
                v.geo2 = row.geo2

                v.save()

    def schemes(self):
        for scheme in FishData.denormalize.schemes():
            try:
                s = Scheme.objects.get(scheme_id=scheme.scheme_id)
            except Exception, e:
                s = Scheme()
            s.scheme_id = scheme.scheme_id
            s.name = scheme.name
            s.total = scheme.total or 0
            s.traffic_light = scheme.traffic_light
            s.save()



    def payments(self):
        for row in FishData.denormalize.payments():
            if not row.pk:
                print "Unknown!"

            try:
                v = Recipient.objects.get(recipient_id=row.recipient_id)
                s = Scheme.objects.get(scheme_id=row.scheme2_id)
                try:
                    p = Payment.objects.get(payment_id=row.id,)
                except:
                    p = Payment(recipient_id=v, payment_id=row.id,)

                try:
                    po = Port.objects.get(name=row.port_name)
                except Exception, e:
                    po = None
                    
                row_dict = row.__dict__
                row_dict['port'] = row_dict.get('port') or ''

                p.amount = row_dict['total_subsidy'] or 0
                if po: p.port = po
                p.year = row_dict['year']
                p.country = row_dict['iso_country']
                p.scheme = s
                p.save()
            except Exception, e:
                print e
                # print row_dict
                print "no vessel"


    def handle_noargs(self, **options):
        # print "ports"
        # self.ports()
        # print "recipient"
        # self.recipient()
        print "schemes"
        self.schemes()
        print "payments"
        self.payments()
