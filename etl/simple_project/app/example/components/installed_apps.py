INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'movies.apps.MoviesConfig',
    'debug_toolbar',
    'corsheaders',
]

CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8080',
                        'http://localhost:8080']