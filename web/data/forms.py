import django.forms
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from frontend.models import Profile
from models import EffData


class DownloadDataForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('name',)

class DataAgreementForm(forms.ModelForm):
    
    data_agreement = forms.BooleanField(required=True, label=_('I Agree to the terms above'))
    data_description = forms.CharField(required=True, label=_('Tell us something about what you plan to do with the data'), widget=forms.Textarea)
    
    class Meta:
        model = Profile
        fields = ('data_agreement', 'data_description',)

class EffSearchForm(forms.Form):
    
    from django.db.models import Count
    
    # YEAR_CHOICES = EffData.objects.all().order_by('yearPaid').values('yearPaid').distinct()
    # YEAR_CHOICES = [(v['yearPaid'],v['yearPaid']) for v in YEAR_CHOICES if v['yearPaid']]
    # YEAR_CHOICES.insert(0, (0, 'All Years'))
    
    query = forms.CharField(required=True, label=_('Search terms'), 
                min_length=2,
                error_messages={
                    'min_length': _('Query must be longer than 2 characters')
                    })
    # yeara = forms.ChoiceField(choices=YEAR_CHOICES, required=False, label=_('Year Allocated'))