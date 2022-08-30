from django.urls import path
from .views import *

app_name = "books"

urlpatterns = [
    path('', booksView.as_view(), name='books'),
    path('detail/', booksdetailView.as_view(), name='book_detail'),
    path('detail/likes/<str:isbn13>', likes, name='likes'),
]
