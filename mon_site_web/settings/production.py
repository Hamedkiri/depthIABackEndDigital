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
