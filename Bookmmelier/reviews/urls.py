from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', reviewsView.as_view(), name='reviews'),
    path('write/', reviewswriteView.as_view(), name='review_write'),
    path('write/searchBooks', searchBooks, name="searchBooks"),
]
