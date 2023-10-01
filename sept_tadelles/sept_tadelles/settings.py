from pathlib import Path
from dotenv import load_dotenv
import logging, os

load_dotenv()

ENV = os.getenv('ENV')
BOT_TOKEN=os.getenv('BOT_TOKEN')
SITE_OWNER_PSEUDO = os.getenv('SITE_OWNER_PSEUDO')
JSON_FILENAME = os.getenv('JSON_FILENAME')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('TOKEN')

if os.getenv('ENV') == "PROD" :
    DEBUG = False
    ALLOWED_HOSTS = ['127.0.0.1', '7tadelles.com']
    CSRF_TRUSTED_ORIGINS = ['https://7tadelles.com']
else :
    DEBUG = True
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'welcome',
    'wiki',
    'soiree',
    'leaderboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sept_tadelles.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sept_tadelles.wsgi.application'
ASGI_APPLICATION = 'sept_tadelles.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv('ENV') == "PROD" :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '7tadelles',
            'USER': '7tadellesuser',
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '',
        }
    }

else :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

### STATIC FILES -------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
if os.getenv("ENV") == "PROD" :
    STATIC_ROOT = '/var/www/html/7tadelles/static/'
else :
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

### MEDIA FILES --------------------------------------------------

if os.getenv('ENV') == "PROD" :
    MEDIA_URL = "/media/"
    MEDIA_ROOT = '/var/www/html/7tadelles/media/'
else :
    MEDIA_URL = "/uploads/"
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')

#-----------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'account/login/'
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'account.User'





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'  # L'adresse de votre serveur SMTP
EMAIL_PORT = 25  # Le port SMTP (587 est généralement utilisé pour TLS)
EMAIL_USE_TLS = False  # Utiliser TLS pour chiffrer la connexion
EMAIL_USE_SSL = False  # Utiliser SSL (désactivé si vous utilisez déjà TLS)





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',  # Nom du fichier de journalisation
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
    'loggers': {
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
    },
}