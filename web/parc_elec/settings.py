import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    os.getenv("PARC_ELEC_FR_BACKEND_SECRET")
    or "django-insecure-&9icj#&rur*)5yel^w3w3wt37-@a$-oj8ub4)_t31o=#!0qb+_"
)

DEBUG = True or not os.getenv("PARC_ELEC_FR_ENV_PRODUCTION")

ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django_vite",
    "power_plants",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "parc_elec.middlewares.HTMXMiddleware",
]

ROOT_URLCONF = "parc_elec.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "parc_elec.wsgi.application"


def get_db_settings():
    if os.getenv("PARC_ELEC_FR_DB_HOST") is not None:
        return {
            "default": {
                "ENGINE": "django.contrib.gis.db.backends.postgis",
                "NAME": os.getenv("PARC_ELEC_FR_DB_NAME"),
                "USER": os.getenv("PARC_ELEC_FR_DB_USER"),
                "PASSWORD": os.getenv("PARC_ELEC_FR_DB_PASSWORD"),
                "HOST": os.getenv("PARC_ELEC_FR_DB_HOST"),
                "PORT": os.getenv("PARC_ELEC_FR_DB_PORT"),
            }
        }

    return {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "osm",
            "USER": "osm",
            "PASSWORD": "osm",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }


DATABASES = get_db_settings()

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

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DJANGO_VITE = {"default": {"dev_mode": DEBUG}}
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR.parent / "app" / "build"]
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
