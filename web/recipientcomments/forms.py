from django import forms
from models import RecipientComment
from django.utils.translation import ugettext_lazy as _

class RecipientCommentForm(forms.ModelForm):
    comment = forms.CharField(required=True, widget=forms.Textarea, help_text=_("""
        <p>
        Comments will be formatted using <a
        href="http://en.wikipedia.org/wiki/Markdown">markdown</a> and
        HTML is allowed.
        </p>
    """))
    
    class Meta:
        model = RecipientComment
        fields = ('comment',)

class RecipientCommentAdminForm(forms.ModelForm):
    
    class Meta:
        model = RecipientComment
        raw_id_fields = ("recipient",)
        # fields = ('comment',)

