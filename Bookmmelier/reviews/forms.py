from django import forms
from django.contrib.auth import authenticate
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget,SummernoteInplaceWidget
from reviews.models import Review


class ReviewwriteFrom(forms.ModelForm):
    title = forms.CharField(max_length=50,label="제목",widget=forms.TextInput(attrs={'placeholder':'제목'}))
    contents = SummernoteTextField()
    rate = forms.ChoiceField(label='별점',widget=forms.RadioSelect,choices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')))
    is_shared = forms.ChoiceField(label='공유',widget=forms.RadioSelect,choices=((1,'공개'),(0,'비공개')))

    field_order = ['title','contents','rate','is_shared']

    class Meta:
        model= Review
        fields = ['title','contents','rate','is_shared']


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title','제목 없음')
        contents = cleaned_data.get('contents','')
        rate = cleaned_data.get('rate','')
        is_shared = cleaned_data.get('is_shared','1')
    
        if not contents:
            self.add_error('contents', '내용을 입력해주세요')
        else:
            if not rate:
                self.add_error('rate', '도서를 평가해주세요')
            else:
                print("문제있음!")
                self.title = title
                self.contents = contents
                self.rate = rate
                self.is_shared = is_shared

