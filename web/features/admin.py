from models import Feature
from django.contrib import admin
# import multilingual
# from sorl.thumbnail.admin import AdminImageMixin

from hvad.admin import TranslatableAdmin

class FeatureAdmin(TranslatableAdmin):
    pass

admin.site.register(Feature, FeatureAdmin)
