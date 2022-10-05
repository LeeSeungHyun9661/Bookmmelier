from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.contrib import auth
from django.views.generic import View
from django.core.paginator import Paginator
from books.models import Book
from debates.models import Debate
from reviews.models import Review
from django.db.models import Q,Avg,Count
from users.models import User

# 메인 페이지 뷰 클래스
class homeView(View):
    def get(self,request):
        context = {}
        template_name = 'bookmmelier_home.html'    

        # # 인기 도서 목록
        bestseller_list = Book.objects.all().annotate(rate=Avg('reviews__rate')).order_by('-rate')[:2]
        context["bestseller_list"] = bestseller_list

        # 추천도서 목록
        recommend_list = Book.objects.all().annotate(rate=Avg('reviews__rate')).order_by('-rate')[:2]
        context["recommend_list"] = recommend_list

        # # 인기 리뷰 목록
        reviews_list = Review.objects.all().annotate(user_cnt=Count('like_users')).order_by('-user_cnt')[:2]
        context["reviews_list"] = reviews_list

        # 각 데이터 수
        context["books_cnt"] = Book.objects.count()
        context["reviews_cnt"] = Review.objects.count()
        context["users_cnt"] = User.objects.count()
        context["debates_cnt"] = Debate.objects.count()

        return render(request, template_name,context)

    def post(self,request):
        return redirect("/")