import django
from django.conf import settings

DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': ':memory:',
    }
}

AIRBRAKE = {
    'PROJECT_ID': "project123",
    'API_KEY': "key123",
    'HOST': 'https://custom-hostname.io',
    'TIMEOUT': 2,
    'ENVIRONMENT': "debug",
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'airbrake': {
            'level': 'ERROR',
            'class': 'airbrake.handler.AirbrakeHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['airbrake'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

settings.configure(AIRBRAKE=AIRBRAKE, DATABASES=DATABASES, LOGGING=LOGGING)
