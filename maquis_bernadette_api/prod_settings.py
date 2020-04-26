from .base_settings import *

DEBUG = False

SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ["*"]


STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
