"""
Takes a list of recipient IDs (one per line) and adds them to a list with pk.


This script always assumes that the list item content type is data.models.Recipient.

TODO: make this more generic.
"""

import sys

import django
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from optparse import make_option

from data.models import Recipient
from listmaker.models import List, ListItem


class ListCreator():
    """
    Stand along class for creating lists programmitically.
    """
    
    def __init__(self, list_id=None, input_ids=None):
        try:
            self.list = List.objects.get(pk=list_id)
        except List.DoesNotExist:
            raise ValueError("List with id %s does not exist" % list_id)
        
        if isinstance(input_ids, list):
            self.ids = input_ids
        else:
            self.ids = [i.strip() for i in input_ids.strip().splitlines()]

    def populate(self):
        for recipient_id in self.ids:
            self.add_recipient(pk=recipient_id)
    
    def add_recipient(self, pk):
        try:
            r = Recipient.objects.get(recipient_id=pk)
            print r
        except Recipient.DoesNotExist:
            print "%s does not exist!" % pk
            return None
        
        ct = ContentType.objects.get_for_model(r)
        if r:
            li = ListItem.objects.get_or_create(list_id=self.list, object_id=r.pk, content_type=ct)
        

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
            make_option('--list',
                dest='list_id',
                ),
            )

    def handle(self, *args, **options):
        
        list_id = options['list_id']
        if not list_id:
            raise ValueError('List ID is required.')
        
        ids = sys.stdin.read()
        x = ListCreator(list_id, ids)
        x.populate()