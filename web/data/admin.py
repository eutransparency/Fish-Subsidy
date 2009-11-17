import data.models
from django.contrib import admin


class IllegalAdmin(admin.ModelAdmin):
    list_display = ('cfr', 'date', 'sanction')
    list_filter = ('date',)    
    
admin.site.register(data.models.illegalFishing, IllegalAdmin)
