import hashlib
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts  import get_current_site
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.views.generic import View
from reviews.models import Review
from users.forms import ForgotPasswordForm, LoginForm,SignupForm, ChangePasswordForm, WithdrawForm, ResetPasswordForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse,JsonResponse

from .models import *
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

# ____ 로그인 기능 ____
class login(View):
    context = {}
    template_name = 'users_login.html'

    # GET -> 처음 로그인 페이지 접급
    def get(self,request):
 
        if request.user.is_authenticated :            
            # 현재 사용자가 로그인 중이라면 메인 화면으로 이동
            return redirect('/')
        else:      
            # 이전 경로에 대한 정보를 받아옴
            self.context["next"] = request.GET.get("next",'')  
            # 로그인폼 지정
            self.context["forms"] = LoginForm()          
            return render(request, self.template_name,self.context)

    # POST -> 로그인 과정 진행
    def post(self,request): 
        # 폼을 기준으로 POST로 전달받은 값 전달
        forms = LoginForm(request.POST)
        print(forms)
        # 폼 입력 조건을 만족한 경우
        if forms.is_valid():
            # 로그인
            auth.login(request,forms.user)
            # 이전 페이지에 대한 정보 전달
            next = request.POST.get("next",'/')
            return JsonResponse({"success":next})
        else:
            # 입력된 폼 조건 불만족 
            return JsonResponse(forms.errors)

# ____ 회원가입 기능 ____
class signup(View):
    context = {}
    template_name = 'users_signup.html'

    # GET -> 처음 회원가입 페이지 접급
    def get(self, request): 
        if request.user.is_authenticated:
            return redirect('/')            
        else:
            # 회원가입 폼 전달
            self.context["forms"] = SignupForm()
            return render(request,self.template_name,self.context)  

    # POST -> 회원가입 과정 진행
    def post(self, request): 
        forms = SignupForm(request.POST)        
        # 회원가입 폼의 입력이 적절한지 확인
        if forms.is_valid():
            user = forms.save(commit=False)                    
            # 사용자 타입은 nomal로 지정
            user.type = "nomal"     
            # 메일 전송 확인   
            if (send_activate_email(request,user)):  
                # 비밀번호 저장
                user.set_password(forms.password)
                # 회원가입 성공
                user.save()
                self.context = {"success":""}
            else:
                # 이메일 전송 실패
                self.context = {"email":"이메일 전송에 실패했습니다."}
        else:
            # 입력된 폼 조건 불만족 
            self.context = forms.errors            
        return JsonResponse(self.context)

# ____ 계정 활성화 기능 ____
class activate(View):
    context = {}
    template_name = 'users_activate.html'
    # GET -> 파라미터가 없는 잘못된 접근
    def get(self,request):
        self.context = {'result' : '올바르지 않은 접근입니다.'}
        return render(request,self.template_name,self.context)

    # GET -> 파라미터가 있는 올바른 접근
    def get(self,request,id,hash):
        # ID나 hash가 입력되지 않은 경우
        if not id or not hash :
            self.context = {'result' : '올바르지 않은 접근입니다.'}
        else :            
            # 존재하는 ID일 경우
            if User.objects.filter(id = id).exists():
                user = User.objects.get(id = id) #사용자 정보 확인
                if user.is_active:
                    self.context = {'result' : '이미 활성화된 계정입니다!'}
                else:
                    if user.hash == hash: #사용자의 해시 값이 일치할 경우
                        user.is_active = 1 #사용 가능 계정으로 설정
                        user.save()
                        self.context = {'result' : '계정이 활성화되었습니다! 페이지를 종료해주세요!'}
                    else :
                        self.context = {'result' : '잘못된 활성화 값이 입력되었습니다!'}
            else:
                self.context = {'result' : '존재하지 않는 계정입니다.'}
        return render(request,self.template_name ,self.context)

# ____ 계정 암호 초기화 페이지 ____
class resetPassword(View):
    context = {}
    template_name = 'users_resetPassword.html'

    # GET -> 파라미터가 있는 올바른 접근
    def get(self,request):        
        id = request.GET.get('id', '') 
        hash = request.GET.get('hash', '') 
        # ID나 hash가 입력되지 않은 경우
        if not id or not hash :
            self.context = {'result' : '올바르지 않은 접근입니다.'}
        else :            
            # 존재하는 ID일 경우
            if User.objects.filter(id = id).exists():
                user = User.objects.get(id = id) #사용자 정보 확인
                if user.hash == hash: #사용자의 해시 값이 일치할 경우
                    self.context['id'] = id
                    self.context["forms"] = ResetPasswordForm()
                else :
                    self.context = {'result' : '잘못된 해쉬 값이 입력되었습니다!'}
            else:
                self.context = {'result' : '존재하지 않는 계정입니다.'}
        return render(request,self.template_name ,self.context)

    def post(self,request):
        forms = ResetPasswordForm(request.POST)        
        if forms.is_valid():
            id = request.POST.get('id', '') 
            if User.objects.filter(id = id).exists():
                #사용자 확인
                user = User.objects.get(id = id) 
                # 암호 재설정
                user.set_password(forms.new_password)

                print("현재 해쉬:" + user.hash)
                # 해쉬 리셋
                enc = hashlib.md5()      
                enc.update(str(random.randint(1000,10000)).encode('utf-8')) #사용자 이메일의 임의 해시값을 생성함
                hash = enc.hexdigest()
                
                print("변경 해쉬:" + hash)

                user.hash = hash
                user.save()

                print("변경된 해쉬:" + user.hash)
                
                self.context = {"success":""}
            else:
                self.context = {'result' : '존재하지 않는 계정입니다.'}

        else:
            print("입력된 폼 조건 불만족 ")
            # 
            self.context = forms.errors
        return JsonResponse(self.context)

# ____ 마이 페이지  ____
class mypage(View):
    context = {}
    template_name = 'users_mypage.html'

    def get(self,request):
        # 사용자가 로그인중인 경우
        if request.user.is_authenticated:
            reviews = Review.objects.filter(user = request.user)[:3]
            self.context["reviews"] = reviews
            return render(request, self.template_name, self.context)

        # 로그인중이 아니면 로그인 화면으로 이동
        else:
            return redirect('/login?next=' + request.path)

    def post(self,request):
        return redirect('/')

# ____ 암호 변경 페이지  ____
class changePassword(View):  
    context = {}
    template_name = 'users_changePassword.html'

    def get(self, request): 
        # 사용자가 로그인중인 경우
        if request.user.is_authenticated:
            if request.user.type == 'nomal':
                # 폼 전달
                self.context["forms"] = ChangePasswordForm()
                return render(request, self.template_name,self.context)
            else:
                """
                사용자가 카카오 로그인을 한 경우에 대한 처리가 필요함                
                """
                return render(request, self.template_name)
        else:
            return redirect('/')

    def post(self, request): 
        if request.user.type == 'nomal':
            forms = ChangePasswordForm(request.POST)
            user = request.user
            forms.setUser(user)
            if forms.is_valid():
                user.set_password(forms.new_password)
                user.save()
                auth.login(request,user,backend='users.backends.MyUserBackend')
                return JsonResponse({"success":""})
            else:
                # 입력된 폼 조건 불만족 
                return JsonResponse(forms.errors)

# ____ 암호 초기화 메일 요청 페이지  ____
class forgotPassword(View):    
    def get(self, request): 
        context = {}
        if request.user.is_authenticated:
            return redirect('/')
        else:
            context["forms"] = ForgotPasswordForm()
            template_name = 'users_forgotPassword.html'
            return render(request, template_name,context)

    def post(self, request): 
            # 폼을 통해 응답받은 결과를 지정
            forms = ForgotPasswordForm(request.POST)
            if forms.is_valid():
                id = forms.id
                email = forms.email

                if User.objects.filter(id = id).exists():
                    user = User.objects.get(id = id)               
                    if user.type == 'nomal':
                        if user.email == email:
                            if (send_reset_email(request,user)):
                                self.context = {"success":""}
                            else:                                
                                self.context = {'result' : '메일 전송에 실패했습니다.'}
                        else:                             
                            self.context = {'result' : '이메일이 올바르지 않습니다.'}
                    else:                         
                        self.context = {'result' : '카카오 로그인 계정입니다.'}
                else:                     
                    self.context = {'result' : '아이디가 존재하지 않습니다.'}
            else:
                self.context = forms.errors
            
            return JsonResponse(self.context)

# ____ 회원 탈퇴 페이지  ____
class withdraw(View):
    def get(self, request): 
        context = {}
        if request.user.is_authenticated:
            if request.user.type == 'nomal':
                context["forms"] = WithdrawForm()
                template_name = 'users_withdraw.html'
                return render(request, template_name,context)
            else:
                return render(request, template_name)
        else:
            return redirect('/login')

    def post(self, request): 
        if request.user.type == 'nomal':
            forms = WithdrawForm(request.POST)
            user = request.user
            forms.setUser(user)
            if forms.is_valid():
                user.delete()          
                auth.logout(request)  
                return JsonResponse({"success":""})
            else:
                # 입력된 폼 조건 불만족 
                return JsonResponse(forms.errors)

# ____ 카카오 회원 탈퇴 페이지  ____
class withdraw_kakao(View):
    def get(self,request):
        template_name ='users_withdraw_kakao.html'
        if request.user.is_authenticated:
            if request.user.type == 'nomal':
                return redirect('mypage/withdraw',template_name)
            else :
                return render(request, )
        else:
            return redirect('/')

    def post(self,request):
            context = {}
            template_name ='users_withdraw_kakao.html'

            input = request.POST['input']
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
            return render(request, template_name,context)

# ____ 사용자 리뷰 목록 페이지  ____
class reviews(View):
    # 페이지 일반 접근
    def get(self,request): 
        # 전체 도서의 DB 연결
        reviews = Review.objects.filter(user = request.user)
        #페이지 확인
        page = int(request.GET.get('page', 1))
        #입력된 검색어 확인
        search_input = request.GET.get('search_input', '') 
        #입력된 검색 유형 확인
        search_type = request.GET.get('search_type', '')

        #ajax로 통신 -> 페이지 또는 검색
        if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': 
             #검색어가 있을 경우 검색어로 필터링
            if search_input:
                #검색어 구분에 따라 리뷰 데이터 필터링
                if search_type == '전체':
                    reviews = Review.objects.filter(
                        Q(book__title__icontains = search_input) | 
                        Q(user__name__icontains = search_input) | 
                        Q(contents__icontains = search_input)
                    )
                elif search_type == '도서':
                    reviews =  Review.objects.filter(Q(book__title__icontains = search_input))
                elif search_type == '작성자':
                    reviews =  Review.objects.filter(Q(user__name__icontains = search_input))
                elif search_type == '내용':
                    reviews =  Review.objects.filter(Q(contents__icontains = search_input))          

            #페이지네이션을 통해 10개씩 페이지로 정리
            paginator = Paginator(reviews, 10)
            #페이지 번호에 따라 페이지네이션 된 결과물 불러오기
            reviews_list = paginator.get_page(page)
            #결과 전송
            return render(request, 'users_mypage_reviews_table.html',{"reviews_list":reviews_list,"search_input":search_input,"search_type":search_type})
        else: #ajax로 통신 아님 -> 기본적인 페이지 접근
            paginator = Paginator(reviews, 10) 
            #페이지 번호에 따라 페이지네이션 된 결과물 불러오기 
            reviews_list = paginator.get_page(page)
            #결과 전송
            return render(request, 'users_mypage_reviews.html',{"reviews_list":reviews_list})  

    def post(request):
        return None

# ____ 사용자 로그아웃 기능  ____
def logout(request):
    auth.logout(request)
    return redirect('/')

# ____ 계정 활성화 요청 링크 발송 기능  ____
def send_activate_email(request,user):
    enc = hashlib.md5()      
    enc.update(str(random.randint(1000,10000)).encode('utf-8')) #사용자 이메일의 임의 해시값을 생성함
    hash = enc.hexdigest()
    user.hash = hash
    domain = get_current_site(request).domain #현재 도메인 주소를 받아옴
    email_contents = f"반갑습니다! {user.name}님\n\n아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/activate/{user.id}/{user.hash}\n\n감사합니다."            
    mail = send_mail(subject='Bookmmelier Account Check', message=email_contents, from_email='dltmdgus@dippingai.com', recipient_list=[user.email]) #메일 작성 후 발송 실행
    return mail

# ____ 암호 초기화 요청 링크 발송 기능  ____
def send_reset_email(request,user):
    domain = get_current_site(request).domain #현재 도메인 주소를 받아옴
    email_contents = f"{user.name}님\n\n아래 링크를 클릭하면 비밀번호 변경 화면으로 이동합니다.\n\n비밀번호 변경 링크 : http://{domain}/resetpassword?id={user.id}&hash={user.hash}\n\n감사합니다."            
    mail = send_mail(subject='Bookmmelier Account Check', message=email_contents, from_email='dltmdgus@dippingai.com', recipient_list=[user.email]) #메일 작성 후 발송 실행
    return mail