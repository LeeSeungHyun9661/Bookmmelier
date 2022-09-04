from django import forms
from django.contrib.auth import authenticate
from reviews.models import User

class LoginForm(forms.Form):
    id = forms.CharField(max_length=15,label="아이디")
    pw = forms.CharField(widget=forms.PasswordInput,label="비밀번호")

    class Meta:
        model= User
    
    def clean(self): 
        cleaned_data = super().clean() 
        id = cleaned_data.get('id')
        pw = cleaned_data.get('pw')

        if not id:
            self.add_error('id', '아이디를 입력해주세요')
        else:
            if not pw:
                self.add_error('pw', '비밀번호를 입력해주세요')
            else:
                try:
                    user = authenticate(id = id,password = pw)
                    if user is not None:             
                        if user.is_active:
                            self.user = user
                        else:
                            self.add_error('id', '이메일을 통한 인증을 완료해주세요.')
                except Exception as e:
                    if e.args[0] == 'Wrong ID':
                        self.add_error('id', '존재하지 않는 아이디입니다.')
                    elif e.args[0] == 'Wrong Password':
                        self.add_error('pw', '비밀번호가 일치하지 않습니다.')
                    else :
                        self.add_error('pw',e)