from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeView.as_view(), name='home'),
    path('', include('users.urls')),
    path('books/', include('books.urls')),
    path('reviews/', include('reviews.urls')),
]
