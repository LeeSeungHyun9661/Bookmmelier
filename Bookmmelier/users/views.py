from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts  import get_current_site
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib import auth
from django.views.generic import View
from .models import *
import hashlib
import random
import re

class loginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        id = request.POST['input_id']
        pw = request.POST['input_pw']
        context = {}

        if not id:
            context = {'result':'아이디를 입력해주세요'}
        else:
            if not pw:
                context = {'result':'비밀번호를 입력해주세요'}
            else:
                try:
                    user = authenticate(id = id,password = pw)  
                    if user is not None:             
                        if user.is_active:
                            auth.login(request,user)
                            return redirect ('/')
                        else:
                            context = {'result':'이메일을 통한 인증을 완료해주세요.'}                        
                except Exception as e:
                    if e.args[0] == 'Wrong ID':
                        context = {'result':'존재하지 않는 아이디입니다..'}
                    elif e.args[0] == 'Wrong Password':
                        context = {'result':'비밀번호가 일치하지 않습니다.'}
        return render(request, 'login.html',context)

class signupView(View):
    def get(self, request):        
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
                                            hash = hash)

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

def logout(request):
    auth.logout(request)
    return redirect('/')