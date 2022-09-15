from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.contrib import auth
from django.views.generic import View
from django.core.paginator import Paginator
from reviews.models import Review
from django.db.models import Q

# 메인 페이지 뷰 클래스
class homeView(View):
    def get(self,request):
        context = {}
        template_name = 'bookmmelier_home.html'        
        return render(request, template_name,context)

    def post(self,request):
        return None