import data.models
import multilingual
from django.contrib import admin


class IllegalAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'dates', 'sanction')

class PaymentInline(admin.TabularInline):
    model = data.models.Payment
    extra = 1

class RecipientAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = ['recipient_id', 'name', 'amount',]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'amount',]

class SchemeAdmin(multilingual.ModelAdmin):
    list_display = ['name','total', 'traffic_light']
    list_filter = ['traffic_light']

admin.site.register(data.models.illegalFishing, IllegalAdmin)
admin.site.register(data.models.DataDownload)
admin.site.register(data.models.FishData)
admin.site.register(data.models.Recipient, RecipientAdmin)
admin.site.register(data.models.Payment, PaymentAdmin)
admin.site.register(data.models.Scheme, SchemeAdmin)
