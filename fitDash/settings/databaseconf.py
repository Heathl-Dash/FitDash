import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE"),
        "NAME": os.environ.get("DB_NAME"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "USER": os.environ.get("DB_USER"),
        "PORT": os.environ.get("DB_PORT"),
    }
}
