from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='amdin'),
    path('', homeView.as_view(), name='home'),
    path('', include('users.urls')),
    path('books/', include('books.urls')),
    path('reviews/', include('reviews.urls')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)