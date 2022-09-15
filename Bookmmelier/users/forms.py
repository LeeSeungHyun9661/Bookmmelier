from django import forms
from django.contrib.auth import authenticate
from reviews.models import User
import re
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    id = forms.CharField(max_length=15,label="아이디")
    password = forms.CharField(widget=forms.PasswordInput,label="비밀번호")
    class Meta:
        model= User
        fields = ['id','password']

    def clean(self): 
        cleaned_data = super().clean() 
        id = cleaned_data.get('id')
        password = cleaned_data.get('password')
        try:
            user = authenticate(id = id, password = password)
            if user is not None:             
                if user.is_active:
                    self.user = user
                else:
                    self.add_error('id', '이메일을 통한 인증을 완료해주세요.')
        except Exception as e:
            if e.args[0] == 'Wrong ID':
                self.add_error('id', '존재하지 않는 아이디입니다.')
            elif e.args[0] == 'Wrong Password':
                self.add_error('id', '비밀번호가 일치하지 않습니다.')
            else :
                self.add_error('id',e)

class SignupForm(forms.ModelForm):
    id = forms.CharField(max_length=15,label="아이디")
    name = forms.CharField(max_length=15,label="이름")
    password = forms.CharField(widget=forms.PasswordInput,label="비밀번호")
    password_check = forms.CharField(widget=forms.PasswordInput,label="비밀번호 확인")
    email = forms.CharField(label="이메일")
    gender = forms.ChoiceField(label='성별',widget=forms.RadioSelect,choices=(('M','남성'),('F','여성')))
    age = forms.IntegerField(label='연령')
    class Meta:
        model= User
        fields = ['id','name','password','password_check','email','gender','age']

    def clean(self): 
        cleaned_data = super().clean() 
        id = cleaned_data.get('id')
        name = cleaned_data.get('name')
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')
        email = cleaned_data.get('email')
        gender = cleaned_data.get('gender')
        age = cleaned_data.get('age')

        if re.search(r'^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{4,15}$/',(id)):
            self.add_error('id','올바른 아이디를 입력해주세요. (영문, 숫자, 언더바, 4~15자)')
        else:            
            self.id = id
            if re.search(r'^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/',(password)):
                self.add_error('password','올바른 비밀번호를 입력해주세요. (영문, 숫자, 특수문자 - 8~20자)')
            else:        
                if password != password_check:
                    self.add_error('password_check','비밀번호가 일치하지 않습니다.')
                else:      
                    self.password = password 
                    self.password_check = password_check                     
                    if not re.search(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',(email)):
                        self.add_error('email','올바른 이메일 주소를 입력해주세요.')
                    else:   
                        self.email = email  
                        if User.objects.filter(id = id).exists():
                            self.add_error('id','이미 사용중인 아이디입니다.')
                        else:
                            if User.objects.filter(email = email).exists():
                                self.add_error('email','이미 사용중인 이메일입니다.')
                            else:
                                self.name = name
                                self.gender = gender
                                self.age = age


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput,label="현재 비밀번호")
    password = forms.CharField(widget=forms.PasswordInput,label="비밀번호")
    password_check = forms.CharField(widget=forms.PasswordInput,label="비밀번호 확인")

    class Meta:
        model= User
        fields = ['current_password','password','password_check']

    def setUser(self,user):
        self.user = user

    def clean(self): 
        cleaned_data = super().clean() 
        current_password = cleaned_data.get('current_password')
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')
        print(self.user.name)
        print(current_password)

        if not check_password(current_password,self.user.password):
            self.add_error('current_password','현재 암호와 일치하지 않습니다.')
        else:
            if password != password_check:
                self.add_error('current_password','새 비밀번호가 일치하지 않습니다.')
            else:
                if current_password == password:
                    self.add_error('current_password','현재 비밀번호와 같은 비밀번호입니다.')
                else:
                    self.new_password = password

class WithdrawForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label="비밀번호")
    password_check = forms.CharField(widget=forms.PasswordInput,label="비밀번호 확인")

    class Meta:
        model= User
        fields = ['password','password_check']

    def setUser(self,user):
        self.user = user

    def clean(self): 
        cleaned_data = super().clean() 
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if not check_password(password,self.user.password):
                self.add_error('password','현재 암호와 일치하지 않습니다.')
        else:
            if password != password_check:
                self.add_error('password_check','확인 비밀번호가 일치하지 않습니다.')