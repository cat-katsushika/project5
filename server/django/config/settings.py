from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])


AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "users.backends.LimitLoginBackend",  # カスタム認証バックエンドに変更
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Application definition

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "axes",
    "django_recaptcha",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # Original apps
    "users",
    "tasks",
    "contacts",
    "payments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.CustomAdminAuthMiddleware",  # Custom middleware
    "axes.middleware.AxesMiddleware",
    "users.middleware.CustomAxesMiddleware",  # Custom middleware
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", BASE_DIR / "templates/allauth"],
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = env.str("DJANGO_STATIC_URL", default="static/")
STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=BASE_DIR / "static")
STATICFILES_DIRS = [
    ("favicon", BASE_DIR / "staticfiles/favicon"),
    ("ogp", BASE_DIR / "staticfiles/ogp"),
    ("fonts", BASE_DIR / "staticfiles/fonts"),
]


MEDIA_URL = env.str("DJANGO_MEDIA_URL", default="media/")
MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default=BASE_DIR / "media")
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

LOGOUT_REDIRECT_URL = "users:home"


REGULAR_EXECUTION_TOKEN = env("REGULAR_EXECUTION_TOKEN")

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")

ONE_TIME_PASSWORD_SECRET = env("ONE_TIME_PASSWORD_SECRET")

CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])


AXES_FAILURE_LIMIT = 10  # ログイン失敗回数の上限
AXES_RESET_ON_SUCCESS = True  # ログイン成功時に失敗回数をリセット

SLACK_API_TOKEN = env("SLACK_API_TOKEN")

DISCORD_WEBHOOK_URL = env("DISCORD_WEBHOOK_URL")

DJANGO_ENV_COLOR = env("DJANGO_ENV_COLOR", default="red")

# for django-recaptcha
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")


SOCIALACCOUNT_PROVICERS = {
    "google": {
        "SCOPE": ["email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
    }
}

SOCIALACCOUNT_QUERY_EMAIL = True

LOGIN_REDIRECT_URL = "users:home"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

ACCOUNT_ADAPTER = "users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "users.adapters.SocialAccountAdapter"
