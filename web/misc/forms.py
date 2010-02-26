import django.forms
from django.conf import settings
from django import forms
# from misc.models import UserProfile
# from contact_form.forms import ContactForm
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class SigninForm (AuthenticationForm):
    user_or_email = django.forms.CharField(label=_(u'Username or email'))
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