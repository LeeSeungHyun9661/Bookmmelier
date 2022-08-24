from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginView.as_view(), name='login'),# 추가 부분
    path('logout/', logout, name='logout'),# 추가 부분
    path('signup/', signupView.as_view(), name='signup'),# 추가 부분
    path('activate/<str:id>/<str:hash>',activateView.as_view(),name="activate"), #이메일을 통한 계정 활성화 링크

]
