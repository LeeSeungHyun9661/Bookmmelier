from django.urls import path
from .views import *

app_name = "books"

urlpatterns = [
    path('', booksView.as_view(), name='books_list'),
    path('detail/', booksdetailView.as_view(), name='book_detail'),
    
    path('detail/like', book_like, name='book_like'),
    path('detail/dislike', book_dislike, name='book_dislike'),
]
