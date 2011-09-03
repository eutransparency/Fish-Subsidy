from models import Feature
from django.contrib import admin
import multilingual
from sorl.thumbnail.admin import AdminImageMixin

class FeatureAdmin(AdminImageMixin, multilingual.ModelAdmin):
    list_display = ('title', 'teaser', 'published','featured')
    list_filter = ('published','featured',)
    prepopulated_fields = {
        # 'slug_en': ('title_en',),
        # 'slug_es': ('title_es',)
        }

admin.site.register(Feature, FeatureAdmin)
