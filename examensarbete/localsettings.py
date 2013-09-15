'''
Created on 12 sep 2013

@author: Martin
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'examensarbete',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'examensarbete',
        'PASSWORD': 'K1ngK0ng',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'D:/Documents/python/examensarbete/templates',
)