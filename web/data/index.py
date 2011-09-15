from djapian import space, Indexer, CompositeIndexer
import xapian

from models import Recipient, Payment, Scheme, Port, illegalFishing, EffData

class RecipientIndexer(Indexer):
    fields = ['pk', 'name', 'geo1', 'geo2','payment.amount']

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
    
    

class EffIndexer(Indexer):
    
    fields = [
        'country',
        'name',
        'measureText',
        'amountEuAllocatedEuro',
        'amountEuPaymentEuro',
        'amountTotalAllocatedEuro',
        'amountTotalPaymentEuro',
        'yearAllocated',
        'yearPaid',
    ]
    
    tags = [
        ('country', 'country'),
        ('name', 'name', 10),
        ('yeara', 'yearAllocated'),
        ('yearp', 'yearPaid'),
    ]
    
space.add_index(EffData, EffIndexer, attach_as='indexer')



    
