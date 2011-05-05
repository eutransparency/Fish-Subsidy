"""
Thin wrapper around managers.denormalize
"""

import django
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.utils import translation
from django.db import connection, backend, models

from data.models import Recipient, Payment, Scheme, Port, FishData

class Command(NoArgsCommand):

    def ports(self):
        FishData.denormalize.ports()

    def recipient(self):
        FishData.denormalize.recipient()

    def schemes(self):
        FishData.denormalize.schemes()

    def payments(self):
        FishData.denormalize.payments()
        
    def handle_noargs(self, **options):
        translation.activate('en')
        
        print "ports"
        self.ports()
        print "recipient"
        self.recipient()
        print "schemes"
        self.schemes()
        print "payments"
        self.payments()
