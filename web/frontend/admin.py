from django.contrib import admin

from models import *

# class ListAdmin(admin.ModelAdmin):
#     inlines = (ListInlines,)
#     list_display = ('name','user',)



admin.site.register(Profile)
# admin.site.register(ListItem)
