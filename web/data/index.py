from djapian import space, Indexer, CompositeIndexer

from models import Recipient, Payment, Scheme, Port, illegalFishing

class RecipientIndexer(Indexer):
    fields = ['name', 'geo1', 'geo2','payment.amount', 'pk']
    tags = [
        ('country', 'country'),
        ('type', 'recipient_type'),
        ('name', 'name', 10),
    ]
space.add_index(Recipient, RecipientIndexer, attach_as='indexer')

class SchemeIndexer(Indexer):
    fields = ['name_en','name_es']
space.add_index(Scheme, SchemeIndexer, attach_as='indexer')

class PortIndexer(Indexer):
    fields = ['name','geo1', 'geo2', 'country']
space.add_index(Port, PortIndexer, attach_as='indexer')

