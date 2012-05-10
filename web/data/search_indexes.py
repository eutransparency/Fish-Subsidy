import datetime
from haystack import indexes
from models import EffData


class EffIndex(indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=10)
    country = indexes.CharField(model_attr='country', faceted=True)
    area1 = indexes.CharField(model_attr='area1')
    area2 = indexes.CharField(model_attr='area2')
    axisText = indexes.CharField(model_attr='axisText')
    actionText = indexes.CharField(model_attr='actionText')
    projectDescription = indexes.CharField(model_attr='projectDescription')
    measureText = indexes.CharField(model_attr='measureText')
    amountEuAllocatedEuro = indexes.FloatField(model_attr='amountEuAllocatedEuro')
    amountEuPaymentEuro = indexes.FloatField(model_attr='amountEuPaymentEuro')
    amountTotalAllocatedEuro = indexes.FloatField(model_attr='amountTotalAllocatedEuro')
    amountTotalPaymentEuro = indexes.FloatField(model_attr='amountTotalPaymentEuro')
    yeara = indexes.CharField(model_attr='yearAllocated', default=0, faceted=True)
    