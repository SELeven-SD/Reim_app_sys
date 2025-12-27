# settings.py
from pathlib import Path
from decouple import config

# ... (其他设置)

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [] # 部署时会被修改

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',
    'reimbursement',
]

# DRF 和 Simple JWT 的配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# 数据库配置
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# ... (其他设置如STATIC_ROOT, MEDIA_ROOT)