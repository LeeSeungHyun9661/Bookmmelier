from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    # 로그인
    path('login/', login.as_view(), name='login'),
    
    # 카카오 로그인
    path("login/kakao/", kakaoLogin, name="kakao-login"),
    
    # 카카오 로그인 - 콜백
    path("login/kakao/callback/", kakaoCallback, name="ukakao-callback"),

    # 비밀번호 찾기 
    path('login/forgotpassword/', forgotPassword.as_view(), name='forgotPassword'),  

    # 비밀번호 찾기 - 비밀번호 변경
    path('resetpassword/',resetPassword.as_view(),name="resetPassword"),

    # 로그아웃
    path('logout/', logout, name='logout'),

    # 회원가입
    path('signup/', signup.as_view(), name='signup'),   

    # 회원가입 - 계정 활성화
    path('activate/<str:id>/<str:hash>',activate.as_view(),name="activate"), 

    # 마이페이지
    path('mypage/', mypage.as_view(), name='mypage'),
    
    # 마이페이지 - 비밀번호 변경
    path('mypage/changePassword', changePassword.as_view(), name='changePassword'),
    
    # 마이페이지 - 회원탈퇴
    path('mypage/withdraw', withdraw.as_view(), name='withdraw'),
    
    # 마이페이지 - 카카오 회원탈퇴
    path('mypage/withdraw_kakao', withdraw_kakao.as_view(), name='withdraw_kakao'),
    
    # 마이페이지 - 사용자 서평 목록
    path('mypage/reviews', reviews.as_view(), name='reviews'),
]
