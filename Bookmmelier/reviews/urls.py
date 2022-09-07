from django.urls import path,include
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', reviews_list_View.as_view(), name='reviews_list'),
    path('detail/', review_detail_View.as_view(), name='review_detail'),
    path('detail/review_delete', review_delete, name='review_delete'),
    path('detail/review_update', review_update_View.as_view(), name='review_update'),

    path('write/', reviews_write_View.as_view(), name='review_write'),
    path('write/modal/searchBooks', review_write_modal_search_Books, name="modal_search_Books"),
    path('write/modal/selectBooks', review_write_modal_select_book, name="modal_select_Books"),
]
