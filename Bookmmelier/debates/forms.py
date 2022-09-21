from django import forms
from django.contrib.auth import authenticate
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget,SummernoteInplaceWidget
from debates.models import Debate

# 리뷰 작성에 따른 모델폼
class DebateCreateFrom(forms.ModelForm):
    title = forms.CharField(label="제목",max_length=50,widget=forms.TextInput(attrs={'placeholder':'제목'}))
    subtitle = forms.CharField(label="부제목",max_length=50,widget=forms.Textarea(attrs={'placeholder':'부제목'}))
    class Meta:
        model= Debate
        fields = ['title','subtitle']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        subtitle = cleaned_data.get('subtitle')

        if not title:
            self.add_error('contents', '제목을 입력해주세요')
        else:
            if not subtitle:
                self.add_error('rate', '도서를 평가해주세요')
            else:
                self.title = title
                self.subtitle = subtitle

