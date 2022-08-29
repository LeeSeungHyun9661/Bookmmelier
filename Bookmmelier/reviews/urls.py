from django.urls import path
from .views import *

# app_name = "books"

urlpatterns = [
    path('', reviewsView.as_view(), name='reviews'),
]
