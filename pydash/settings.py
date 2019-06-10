import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '****'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django_python3_ldap',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pydash.core.apps.CoreConfig',
    'pydash.mail_notifications',
    'pydash.auth_manager',
    'pydash.profiles_manager.apps.ProfilesManagerConfig'
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

ROOT_URLCONF = 'pydash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pydash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = ['django_python3_ldap.auth.LDAPBackend', 'django.contrib.auth.backends.ModelBackend']

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/' + 'static'
MEDIA_ROOT = BASE_DIR + '/' + 'media'
MEDIA_URL = '/media/'
UPLOAD_TO_PROFILE_MODEL_IMAGE_FIELD_NAME='profile_images'
PROFILE_IMAGES_DIR_PATH = MEDIA_ROOT + '/' + UPLOAD_TO_PROFILE_MODEL_IMAGE_FIELD_NAME
DEFAULT_IMAGE_FILENAME = 'default.jpg'

# ldap3
LDAP_SERVER = 'ldap.com'
LDAP_SEARCH_BASE = 'ou=usuarios,dc=matriz,dc=teste,dc=com,dc=br'

# DJANGO-PYTHON3-LDAP
LDAP_AUTH_URL = "ldap://ldap.example.com.br:389"
LDAP_AUTH_SEARCH_BASE = "ou=usuarios,dc=matriz,dc=example,dc=com,dc=br"

LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "gecos",
    "last_name": "sn",
    "email": "mail",
}

# MAIL SETTINGS
EMAIL_USE_SSL = False
EMAIL_PORT = 25
EMAIL_HOST = 'mail.example.com.br'
DEFAULT_FROM_EMAIL = 'dashboard@example.com.br'
