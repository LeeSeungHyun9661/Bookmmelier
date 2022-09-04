import hashlib
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts  import get_current_site
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.views.generic import View
from users.forms import LoginForm

from .models import *
import os
import requests
import random
import re

KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": '7e50c549e6c27570c3528a7e48425019',
    "KAKAO_REDIRECT_URI": 'http://localhost:8000/login/kakao/callback/',
    "KAKAO_CLIENT_SECRET_KEY": 'FFSplBr72EiMHvaWeAWFFkxpYNssGFtD', 
}
kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

class loginView(View):
    def get(self,request):
        if request.user.is_authenticated :
            return redirect('/')
        else:            
            form = LoginForm
            return render(request, 'login.html',{'form': form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request,form.user)
            return redirect('/')
        return render(request, 'login.html',{'form': form})

def kakaoLogin(request):
    client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
    redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
    uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(uri)

def kakaoCallback(request):
    code = request.GET['code']
    # if not code:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

    request_data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_uri': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
        'code': code,
    }
    token_headers = {
    'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

    token_json = token_res.json()
    access_token = token_json.get('access_token')

    # if not access_token:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    access_token = f"Bearer {access_token}"

    auth_headers = {
        "Authorization": access_token,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
    user_info_json = user_info_res.json()

    social_type = 'kakao'
    social_id = f"{social_type}_{user_info_json.get('id')}"

    kakao_account = user_info_json.get('kakao_account')
    # if not kakao_account:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

    email = kakao_account.get('email')
    nickname = kakao_account.get('profile').get('nickname')
    gender = kakao_account.get('gender')
    age_range = kakao_account.get('age_range')

    if not User.objects.filter(id = social_id).exists():
        user = User.objects.create_user(
            id=social_id,
            name=nickname,
            password = None,
            email=email,
            gender=gender,
            age=age_range,
            hash = None,
            type = social_type)
        user.is_active = 1 #사용 가능 계정으로 설정
        user.save()
    else:
        user = User.objects.get(id = social_id)        
    auth.login(request,user,backend='users.backends.MyUserBackend')
    return redirect('/')

class signupView(View):
    def get(self, request): 
        if request.user.is_authenticated:
            return redirect('/')            
        else:
            return render(request,'signup.html')  

    def post(self, request):
        id = request.POST['input_id']
        name = request.POST['input_name']
        pw = request.POST['input_pw']
        pw_check = request.POST['input_pw_check']
        email = request.POST['input_email']
        gender = request.POST['input_gender']
        age = request.POST['input_age']

        context = {}
        if not id or not name or not pw or not pw_check or not email or not gender or not age:
            context = {'result':'모든 입력란을 채워주세요!'}
        else:
            print(id)
            if re.search(r'^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{4,15}$/',(id)):
                context = {'result':'올바른 아이디를 입력해주세요. (영문, 숫자, 언더바, 4~15자)'}
            else:
                if re.search(r'^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/',(pw)):
                    context = {'result':'올바른 비밀번호를 입력해주세요. (영문, 숫자, 특수문자 - 8~20자)'}
                else:
                    if pw != pw_check:
                        context = {'result':'비밀번호가 일치하지 않습니다.'}
                    else:
                        if not re.search(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',(email)):
                            context = {'result':'올바른 이메일 주소를 입력해주세요.'}
                        else:        
                            if User.objects.filter(id = id).exists():
                                context = {'result':'이미 사용중인 아이디입니다.'}
                            else:
                                if User.objects.filter(email = email).exists():
                                    context = {'result':'이미 사용중인 이메일입니다.'}
                                else:
                                    enc = hashlib.md5()      
                                    enc.update(str(random.randint(1000,10000)).encode('utf-8')) #사용자 이메일의 임의 해시값을 생성함
                                    hash = enc.hexdigest()     

                                    domain = get_current_site(request).domain #현재 도메인 주소를 받아옴
                                    email_contents = f"반갑습니다! {name}님\n\n아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/activate/{id}/{hash}\n\n감사합니다."            
                                    mail = send_mail(subject='Bookmmelier Account Check', message=email_contents, from_email='dltmdgus@dippingai.com', recipient_list=[email]) #메일 작성 후 발송 실행
                                    
                                    if(mail) : #메일 전송이 성공적으로 완료된 경우
                                        User.objects.create_user(
                                            id=id,
                                            name=name,
                                            password=pw,
                                            email=email,
                                            gender=gender,
                                            age=age,
                                            hash=hash,
                                            type = 'nomal')

                                        context = {'result':'회원가입이 완료되었습니다.'}
                                        return redirect('/login')
                                    else:
                                        context = {'result':'메일 전송 실패!'}
        return render(request,'signup.html',context)

class activateView(View):
    def get(self,request):
        context = {'result' : '올바르지 않은 접근입니다.'}
        return render(request,'activate.html',context)

    def get(self,request,id,hash):
        context = {}
        if not id or not hash :
            context = {'result' : '올바르지 않은 접근입니다.'}
        else :
            if User.objects.filter(id = id).exists():
                user = User.objects.get(id = id) #사용자 정보 확인
                if user.is_active:
                    context = {'result' : '이미 활성화된 계정입니다!'}
                else:
                    if user.hash == hash: #사용자의 해시 값이 일치할 경우
                        user.is_active = 1 #사용 가능 계정으로 설정
                        user.save()
                        context = {'result' : '계정이 활성화되었습니다! 페이지를 종료해주세요!'}
                    else :
                        context = {'result' : '잘못된 활성화 값이 입력되었습니다!'}
            else:
                context = {'result' : '존재하지 않는 계정입니다.'}
        return render(request,'activate.html' ,context)

class mypageView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'mypage.html')
        else:
            return redirect('/')

class changePassword(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.type == 'nomal':
                return render(request, 'changePassword.html')
            else:
                return redirect('/')
        else:
            return redirect('/')

    def post(self,request):
        input_pw = request.POST['input_pw']
        change_pw = request.POST['change_pw']
        change_pw_check = request.POST['change_pw_check']

        context = {}

        if not input_pw or not change_pw or not change_pw_check:
            context = {'result':'모든 입력란을 채워주세요!'}
        else:
            user = request.user
            if check_password(input_pw,user.password):
                if input_pw == change_pw:
                    context = {'result':'변경 비밀번호가 현재 비밀번호와 일치합니다.'}
                else:
                    if re.search(r'^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/',(change_pw)):
                        context = {'result':'올바른 비밀번호를 입력해주세요. (영문, 숫자, 특수문자 - 8~20자)'}
                    else:
                        if change_pw == change_pw_check:
                            user.set_password(change_pw)
                            user.save()
                            auth.login(request,user,backend='users.backends.MyUserBackend')
                            return redirect("/")
                        else:
                            context = {'result':'새 비밀번호가 일치하지 않습니다.'}
            else:
                context = {'result':'현재 비밀번호가 일치하지 않습니다.'}

        return render(request, 'changePassword.html',context)

class withdraw(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.type == 'nomal':
                return render(request, 'withdraw.html')
            else :
                return redirect('mypage/withdraw_kakao')
        else:
            return redirect('/')

    def post(self,request):
            input_pw = request.POST['input_pw']
            input_pw_check = request.POST['input_pw_check']
            context = {}

            if not input_pw or not input_pw_check:
                context = {'result':'비밀번호를 입력해주세요!'}
            else:
                user = request.user
                if input_pw == input_pw_check:
                    if check_password(input_pw,user.password):
                        user.delete()          
                        auth.logout(request)             
                        return redirect("/")
                    else:
                        context = {'result':'비밀번호가 올바르지 않습니다.'}                   
                else:
                    context = {'result':'비밀번호가 일치하지 않습니다.'}

            return render(request, 'withdraw.html',context)

class withdraw_kakao(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.type == 'nomal':
                return redirect('mypage/withdraw')
            else :
                return render(request, 'withdraw_kakao.html')
        else:
            return redirect('/')

    def post(self,request):
            input = request.POST['input']
            context = {}
            if not input:
                context = {'result':'확인 문장을 입력해주세요'}
            else:
                user = request.user
                if input == '회원탈퇴':
                    user.delete()          
                    auth.logout(request)             
                    return redirect("/")                  
                else:
                    context = {'result':'확인 문장이 일치하지 않습니다.'}
            return render(request, 'withdraw_kakao.html',context)

def logout(request):
    auth.logout(request)
    return redirect('/')

