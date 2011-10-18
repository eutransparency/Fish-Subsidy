import datetime
from haystack.indexes import *
from haystack import site
from models import EffData


class EffIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name', boost=10)
    country = CharField(model_attr='country', faceted=True)
    
    area1 = CharField(model_attr='area1')
    area2 = CharField(model_attr='area2')
    
    axisText = CharField(model_attr='axisText')
    actionText = CharField(model_attr='actionText')
    projectDescription = CharField(model_attr='projectDescription')
    measureText = CharField(model_attr='measureText')
    
    amountEuAllocatedEuro = FloatField(model_attr='amountEuAllocatedEuro')
    amountEuPaymentEuro = FloatField(model_attr='amountEuPaymentEuro')
    amountTotalAllocatedEuro = FloatField(model_attr='amountTotalAllocatedEuro')
    amountTotalPaymentEuro = FloatField(model_attr='amountTotalPaymentEuro')
    
    
    yeara = CharField(model_attr='yearAllocated', default=0, faceted=True)
    

site.register(EffData, EffIndex)