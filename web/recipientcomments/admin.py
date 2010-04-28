from django.contrib import admin

from models import RecipientComment
import forms

class RecipientCommentAdmin(admin.ModelAdmin):
    list_display = ('recipient','user','published')
    form = forms.RecipientCommentAdminForm
    raw_id_fields = ("recipient",)

admin.site.register(RecipientComment, RecipientCommentAdmin)
