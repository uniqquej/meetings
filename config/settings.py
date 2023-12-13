from pathlib import Path
import os
import environ
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    #install
    "drf_yasg",
    "rest_framework",
    "rest_framework_simplejwt",
    "debug_toolbar",
    "corsheaders",
    
    #my app
    "user",
    "post",
    "chat",
    "group",
    "recruitment",
]

ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "JWT Token"
        }
    },
    'SECURITY_REQUIREMENTS': [{
        'BearerAuth': []
    }]
}

CORS_ORIGIN_WHITELIST = ('http://127.0.0.1:3000', 'http://localhost:3000')

INTERNAL_IPS = ('127.0.0.1')

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"
