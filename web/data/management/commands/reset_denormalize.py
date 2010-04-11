"""
Thin wrapper around managers.denormalize
"""

import django
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db import connection, backend, models
from data.models import Recipient, Payment, Scheme, FishData

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        cursor = connection.cursor()
        for table in ('data_recipient', 'data_payment', 'data_scheme', 'data_port'):
            cursor.execute("""
              DROP TABLE %s;
            """ % (table,))
            