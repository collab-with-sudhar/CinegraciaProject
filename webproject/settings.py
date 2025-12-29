"""
Django settings for webproject project.
Hosted on Azure VM with Supabase Database & Storage.
"""

from pathlib import Path
import os
import dj_database_url
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# SECURITY: Secrets & Debug
# ==========================================
# Read from .env, fallback to insecure key only for local dev
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-this')

# Set DEBUG to False in production (loaded from .env)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allow Cloudflare domain and localhost
ALLOWED_HOSTS = ['cinema.nix-ai.dev', 'localhost', '127.0.0.1']

# Trusted origins for Cloudflare to prevent CSRF errors
CSRF_TRUSTED_ORIGINS = ['https://cinema.nix-ai.dev']


# ==========================================
# Applications & Middleware
# ==========================================
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic', # Must be before django.contrib.staticfiles
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'storages', # For Supabase Media

    # My Apps
    'websiteapp',
    'register',
    'moviedetail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Handles CSS/JS in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

ROOT_URLCONF = 'webproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Fixed path syntax
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

WSGI_APPLICATION = 'webproject.wsgi.application'


# ==========================================
# Database (Supabase)
# ==========================================
# This automatically parses the DATABASE_URL from .env
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}


# ==========================================
# Passwords & Auth
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================
# Internationalization
# ==========================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # Set to your time zone
USE_I18N = True
USE_TZ = True


# ==========================================
# Static Files (CSS, JS) - Managed by Whitenoise
# ==========================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Enable Whitenoise compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==========================================
# Media Files (Images) - Managed by Supabase (S3 Compatible)
# ==========================================
if DEBUG:
    # Local storage for development
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # Supabase Storage for Production
    AWS_ACCESS_KEY_ID = os.environ.get('SUPABASE_ACCESS_KEY_ID') # "S3 Access Keys" in Supabase
    AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'media' # Name of your bucket in Supabase
    AWS_S3_ENDPOINT_URL = os.environ.get('SUPABASE_S3_ENDPOINT') # e.g. https://xyz.supabase.co/storage/v1/s3
    
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = False
    
    # Use S3 for Media, but Keep Whitenoise for Static
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# ==========================================
# Session & Logout
# ==========================================
AUTO_LOGOUT = {'IDLE_TIME': 6000}
SESSION_COOKIE_AGE = 6000
SESSION_COOKIE_SECURE = True # Set True for HTTPS (Cloudflare)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================
# Email Configuration
# ==========================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')