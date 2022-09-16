from . import *

SECRET_KEY="?~L/ixBS\\@.-PzvwL9k}yK@^"
DEBUG = False
ALLOWED_HOSTS = ["138.68.148.124"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'mon_site_web',
        'USER':'hamedkiri',
        'PASSWORD':'Kiri66394716',
        'HOST':'',
        'PORT':'5432',
        'ATOMIC_REQUESTS':True,
    }
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://f7faa7e6a2f44e1db6cea56b252dc4d7@o1413233.ingest.sentry.io/6752891",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
