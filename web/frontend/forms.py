import django.forms
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm

from models import Profile


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('name',)

class DataAgreementForm(forms.ModelForm):
    
    data_agreement = forms.BooleanField(required=True, label=_('I Agree to the terms above'))
    data_description = forms.CharField(required=True, label=_('Tell us something about what you plan to do with the data'), widget=forms.Textarea)
    
    class Meta:
        model = Profile
        fields = ('data_agreement', 'data_description',)




class SigninForm (AuthenticationForm):
    # user_or_email = django.forms.CharField(label=_(u'Username or email'))
    remember_me = django.forms.BooleanField(widget=django.forms.CheckboxInput(),
                           label=_(u'Remember me'))


class CreateAccountForm(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service and makes sure the email address is unique.

    """
    
    def clean_email(self):
       """
       Validate that the supplied email address is unique for the
       site.

       """
       if User.objects.filter(email__iexact=self.cleaned_data['email']):
           raise django.forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
       return self.cleaned_data['email']