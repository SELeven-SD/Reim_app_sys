# reimbursement_system/settings.py
from pathlib import Path
from decouple import config
import dj_database_url
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'axes',
    'reimbursement',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reimbursement_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'reimbursement_system.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/api/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# CORS 配置 - 允许所有192网段访问
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://211\.87\.236\.94(:\d+)?$",
    r"^http://192\.168\.\d{1,3}\.\d{1,3}(:\d+)?$",
    r"^http://localhost(:\d+)?$",
    r"^http://127\.0\.0\.1(:\d+)?$",
]

CORS_ALLOW_CREDENTIALS = True

# CSRF 配置 - 信任的来源（Django 4.0+必需）
CSRF_TRUSTED_ORIGINS = [
    'http://211.87.236.94',
    'http://211.87.236.94:8088',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# 使用Nginx代理的Host头
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── 安全响应头配置 ──────────────────────────────────────────────────────────
# 禁止浏览器将响应内容嗅探为其他 MIME 类型
SECURE_CONTENT_TYPE_NOSNIFF = True
# 禁止被任何页面嵌入为 <iframe>（防点击劫持）
X_FRAME_OPTIONS = 'DENY'

# ── Admin 路径通过环境变量配置（不使用默认 admin/ 路径）───────────────────────
ADMIN_URL = config('ADMIN_URL', default='manage-panel/')

# ── django-axes 防暴力破解配置 ────────────────────────────────────────────
AXES_FAILURE_LIMIT = 5           # 允许最多 5 次失败
AXES_COOLOFF_TIME = 24           # 锁定 24 小时
AXES_LOCK_OUT_AT_FAILURE = True  # 超限后锁定
AXES_LOCKOUT_PARAMETERS = ['ip_address', 'username']  # 按 IP + 用户名双维度锁定
AXES_RESET_ON_SUCCESS = True     # 登录成功后自动解锁

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]
