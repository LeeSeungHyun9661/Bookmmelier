from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path('login/', login.as_view(), name='login'),
    path("login/kakao/", kakaoLogin, name="kakao-login"),
    path("login/kakao/callback/", kakaoCallback, name="ukakao-callback"),
    path('logout/', logout, name='logout'),
    path('signup/', signup.as_view(), name='signup'),  

    path('mypage/', mypage.as_view(), name='mypage'),
    path('mypage/changePassword', changePassword.as_view(), name='changePassword'),
    path('mypage/withdraw', withdraw.as_view(), name='withdraw'),
    path('mypage/withdraw_kakao', withdraw_kakao.as_view(), name='withdraw_kakao'),
    path('mypage/reviews', reviews.as_view(), name='reviews'),   
    
    path('activate/<str:id>/<str:hash>',activate.as_view(),name="activate"), #이메일을 통한 계정 활성화 링크
]
