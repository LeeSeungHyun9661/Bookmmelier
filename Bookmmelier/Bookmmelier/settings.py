from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

# Auth 기능을 연결할 유저 모델을 지정
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.MyUserBackend',
)

ALLOWED_HOSTS = []

# 사용중인 앱 목록
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_summernote',
    'bootstrap4',
    'users',
    'books',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'Bookmmelier.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'C:\DippingAI\Bookmmelier\Bookmmelier', 'templates')], #템플릿 위치 지정
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

#데이터 베이스 경로 설정
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'Bookmmelier',
#         'USER': 'dipping',
#         'PASSWORD': '$qnramffldp03)@',
#         'HOST': 'dippingai.com',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
SECRET_KEY = 'django-insecure-$clx2x7t60=er0!e+r@gnq(2bdqs$#*%v1!a!uv7pce4h3vp3f'
WSGI_APPLICATION = 'Bookmmelier.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'Bookmmelier','static'),] 
STATIC_ROOT = os.path.join(BASE_DIR,'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 이메일 발송을 위한 GMAIL smtp 설정
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dltmdgus9661@gmail.com' # GMAIL 주소
EMAIL_HOST_PASSWORD = 'zzvrwardbcqwdwpj' # GMAIL에서 사용되는 앱 비밀번호
DEFAULT_FROM_EMAIL = 'DippingAI'

# 세션 만료 설정
SESSION_EXPIRE_SECONDS = 3600 #마지막 활동 1시간 후 로그인 종료됨
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = '/'

# Summernote 설정
SUMMERNOTE_CONFIG = {
    'iframe': False,
    'summernote': {
        'airMode': False,
        'width': '80%',
        'height': '480',
        'lang': 'ko-KR',
    },
}

# Summernote 기능을 위한 MEDIA 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# 메시지 기능 설정
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

