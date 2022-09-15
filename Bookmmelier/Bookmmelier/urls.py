from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include

from .views import *

urlpatterns = [
    # 관리자
    path('admin/', admin.site.urls, name='amdin'),
    # 메인 페이지
    path('', homeView.as_view(), name='home'),    
    # 사용자
    path('', include('users.urls')),
    # 도서
    path('books/', include('books.urls')),    
    # 서평
    path('reviews/', include('reviews.urls')),    
    # 토폰
    path('debates/', include('debates.urls')),
    # 서머노트 기반 url
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)