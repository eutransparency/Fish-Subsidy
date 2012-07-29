#-*- coding: utf-8 -*-

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.split(PROJECT_PATH)[0]

# Django settings for web project.
from django.utils.translation import ugettext_lazy as _

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static/')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    MEDIA_ROOT,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1k-$iny+hp35t*_mgf2fpgck&3g4el_sw1z8dc^l3r5=o+%_qg'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'babeldjango.middleware.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',    
    'django_notify.middleware.NotificationsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'multilingual.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'web.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',    
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'data',
    'search',
    'stats',
    'feeds',
    'misc',
    'tagging',
    'pagination',
    'registration',
    'features',
    'listmaker',
    'profiles',
    'frontend',
    'django_notify',
    'rosetta',
    'johnny',
    'multilingual',
    'multilingual.flatpages',
    'babeldjango',
    'djapian',
    'recipientcomments',
    'typogrify',
    'sorl.thumbnail',
    'haystack',
    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'mptt',
    'cms',
    'twitterfeed',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.core.context_processors.static',
    'multilingual.context_processors.multilingual',
    'data.context_processors.country',
    'data.context_processors.ip_country',
    'features.context_processors.featured_items',
    'listmaker.context_processors.list_items',
    'django_notify.context_processors.notifications',
    'misc.context_processors.header_class',
    'features.context_processors.featured_items',
    'twitterfeed.context_processors.latest_tweets',
)


DEFAULT_CHARSET = "utf-8" 
NOTIFICATIONS_STORAGE = 'session.SessionStorage'

ugettext = lambda s: s

LANGUAGES = (
  ('en', ugettext('English')),
  ('es', ugettext('Español'.decode('utf8'))),
  ('fr', ugettext('Français'.decode('utf8'))),
  ('de', ugettext('Deutsch'.decode('utf8'))),
)
MULTILINGUAL_FALLBACK_LANGUAGES = ['en', 'es', 'fr', 'de',]
LANGUAGE_CODE = 'en'
DEFAULT_LANGUAGE = 1

TWITTER_USER = "fishsubsidy"
TWITTER_TIMEOUT = 300

AUTH_PROFILE_MODULE = 'frontend.Profile'
LOGIN_URL = '/login/'

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_TIMEOUT = 1209600
REGISTRATION_BACKEND = "registration.backends.default.DefaultBackend"
ACCOUNT_ACTIVATION_DAYS = 15

DEFAULT_FROM_EMAIL = "team@fishsubsidy.org"

DJAPIAN_DATABASE_PATH = "xapian.db"
DJAPIAN_STEMMING_LANG = "multi"

CACHE_MIDDLEWARE_SECONDS = 6


STATS_PATH = ROOT_PATH + '/data/stats'
DEFAULT_YEAR = 0

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE' : 'xapian_backend.XapianEngine',
        'PATH' : 'xapian-haystack.db',
        'INCLUDE_SPELLING': True,
    }
}
