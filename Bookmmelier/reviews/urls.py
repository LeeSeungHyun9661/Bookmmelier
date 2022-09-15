from django.urls import path,include
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', reviews_list_View.as_view(), name='list'),
    path('detail', review_detail_View.as_view(), name='detail'),
    path('detail/review/delete', review_delete, name='delete'),
    path('detail/review/update', review_update_View.as_view(), name='update'),
    path('detail/comment/upload', comment_upload, name='comment_upload'),
    path('detail/comment/update', comment_update, name='comment_update'),
    path('detail/comment/delete', comment_delete, name='comment_delete'),
    path('detail/like', review_like, name='like'),
    path('detail/dislike', review_dislike, name='dislike'),

    path('write/', reviews_write_View.as_view(), name='write'),
    path('write/modal/searchBooks', review_write_modal_search_Books, name="modal_search_Books"),
    path('write/modal/selectBooks', review_write_modal_select_book, name="modal_select_Books"),
]
