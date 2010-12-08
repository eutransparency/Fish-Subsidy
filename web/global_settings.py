#
#-*- coding: utf-8 -*-

# Django settings for web project.
from django.utils.translation import ugettext_lazy as _

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1k-$iny+hp35t*_mgf2fpgck&3g4el_sw1z8dc^l3r5=o+%_qg'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
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
    'multilingual.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'web.urls'


INSTALLED_APPS = [
    'django.contrib.auth',
    # 'django.contrib.comments',    
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.redirects',
    'data',
    'search',
    'stats',
    'feeds',
    'misc',
    'graphs',
    'tagging',
    'pagination',
    'registration',
    'features',
    # 'listmaker',
    'profiles',
    'frontend',
    'django_notify',
    'rosetta',
    'johnny',
    'multilingual',
    'multilingual.flatpages',
    'babeldjango',
    'djapian',
    'recipientcomments'
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'multilingual.context_processors.multilingual',  
    'data.context_processors.country',
    'data.context_processors.ip_country',  
    'misc.context_processors.latest_tweet',
    'features.context_processors.featured_items',
    'listmaker.context_processors.list_items',
    'django_notify.context_processors.notifications',  
)


DEFAULT_CHARSET = "utf-8" 
NOTIFICATIONS_STORAGE = 'session.SessionStorage'

ugettext = lambda s: s

LANGUAGES = (
  ('en', ugettext('English')),
  ('es', ugettext('Español'.decode('utf8'))),
  ('fr', ugettext('Français'.decode('utf8'))),
)
MULTILINGUAL_FALLBACK_LANGUAGES = ['en', 'es', 'fr']
LANGUAGE_CODE = 'en'
DEFAULT_LANGUAGE = 1

TWITTER_USER = "fishsubsidy"
TWITTER_TIMEOUT = 3600

AUTH_PROFILE_MODULE = 'frontend.Profile'
LOGIN_URL = '/login/'

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_TIMEOUT = 1209600
REGISTRATION_BACKEND = "registration.backends.default.DefaultBackend"
ACCOUNT_ACTIVATION_DAYS = 15

DEFAULT_FROM_EMAIL = "team@fishsubsidy.org"

DJAPIAN_DATABASE_PATH = "xapian.db"
DJAPIAN_STEMMING_LANG = "multi"


CACHE_MIDDLEWARE_SECONDS = 30
