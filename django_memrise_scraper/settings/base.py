"""
Django settings for django_memrise_scraper project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from typing import Dict

import dj_database_url

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "v7ow)+p_5+qe(&n3(!i!=jacnl(r5q^&9rk4j#9dp=sp$igk^)"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "memrise.apps.MemriseConfig",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_memrise_scraper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ROOT_DIR / "templates", ROOT_DIR / "front" / "dist"],
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

WSGI_APPLICATION = "django_memrise_scraper.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
os.environ.setdefault("DATABASE_URL", f"sqlite:///db.sqlite3")
DATABASES = {"default": dj_database_url.config(conn_max_age=60)}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Путь до каталога ресурсов.
RESOURSES = ROOT_DIR / "resources"
FIXTURE_DIRS = [RESOURSES / "fixtures"]
# Хранилище курсов и полученных файлов сервиса.
STORAGE = Path(os.getenv("STORAGE", RESOURSES / "logs"))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = RESOURSES / "static"
FRONT_STATIC_ROOT = ROOT_DIR / "front" / "dist"

# Наименование сервиса.
SERVICE_IDENTIFIER = "django_memrise_scraper"
# <editor-fold desc="Logging">
LOG_FILE = STORAGE / f"{SERVICE_IDENTIFIER}.log"
LOG_INTO_FILE = os.environ.setdefault("LOG_INTO_FILE", "0") == "1"
LOG_LEVEL = os.environ.setdefault("LOG_LEVEL", "DEBUG")
LOG_FORMATTER_CONSOLE = os.environ.setdefault("LOG_FORMATTER_CONSOLE", "simple")
LOG_FORMATTER_FILE = os.environ.setdefault("LOG_FORMATTER_FILE", "json")

handlers = ["console"]
if LOG_INTO_FILE:
    handlers.append("file")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[%(asctime)s] [%(levelname)s] %(message)s"},
        "verbose": {
            "format": (
                "[%(asctime)s][%(process)d][%(levelname)s]"
                "[%(pathname)s/%(filename)s:%(lineno)s] %(message)s"
            )
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": (
                "%(levelname)s %(asctime)s %(message)s "
                "%(funcName)s %(pathname)s %(lineno)s %(name)s"
            ),
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": LOG_FORMATTER_CONSOLE,
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": LOG_FORMATTER_FILE,
        },
    },
    "loggers": {
        "django": {"handlers": handlers, "level": "INFO", "propagate": True},
        "django_memrise_scraper": {
            "handlers": handlers,
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "memrise": {"handlers": handlers, "level": LOG_LEVEL, "propagate": True},
    },
}
# </editor-fold>


MEMRISE_COOKIES: Dict = dict(
    sessionid_2=os.getenv("SESSION_ID", ""),
    i18next="en",
    csrftoken=os.getenv("CSRF_TOKEN", ""),
    cookieconsent_status="allow",
)

USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/60.0.3112.113 Safari/537.36"
)

MEMRISE_HOST = "https://app.memrise.com"
