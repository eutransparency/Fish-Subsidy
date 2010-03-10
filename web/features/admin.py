from models import Feature
from django.contrib import admin

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'teaser', 'published','featured')
    list_filter = ('published','featured',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Feature, FeatureAdmin)
