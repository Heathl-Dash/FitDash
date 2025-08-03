INSTALLED_APPS = []

DEFAULT = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

FIRST_PARTY = ["fitCore.apps.FitcoreConfig"]

THIRD_PARTY = [
    "corsheaders",
    "rest_framework",
    "simple_history",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]

INSTALLED_APPS += DEFAULT
INSTALLED_APPS += FIRST_PARTY
INSTALLED_APPS += THIRD_PARTY
