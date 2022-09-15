from django.urls import path
from .views import *

app_name = "debates"

urlpatterns = [
    path('', debates_list.as_view(), name='list'),
    path('create', debates_create.as_view(), name='create'),

    path('detail', debates_detail.as_view(), name='detail'),
    path('debates/message/upload', debates_upload_message, name='upload_message'),
    path('debates/message/delete', debates_delete_message, name='delete_message'),
    path('debates/message/update', debates_update_message, name='update_message'),
]
