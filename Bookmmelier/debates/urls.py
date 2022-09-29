from django.urls import path
from .views import *

app_name = "debates"

urlpatterns = [
    path('', debates_list.as_view(), name='list'),
    path('modal/searchBooks', debates_list_search_Books, name="list_search_Books"),
    path('modal/selectBooks', debates_list_select_book, name="list_select_Books"),

    path('create', debates_create.as_view(), name='create'),
    path('delete', debates_delete, name='delete'),
    path('update', debates_update.as_view(), name='update'),
    path('create/modal/searchBooks', debates_list_search_Books, name="create_search_Books"),
    path('create/modal/selectBooks', debates_create_select_book, name="create_select_Books"),

    path('detail', debates_detail.as_view(), name='detail'),
    path('debates/message/delete', debates_delete_message, name='delete_message'),
    path('debates/message/update', debates_update_message, name='update_message'),    

]
