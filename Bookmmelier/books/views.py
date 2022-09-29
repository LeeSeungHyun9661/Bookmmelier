from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Avg,Count,F
from debates.models import Debate
from reviews.models import Review
from .models import *
from django.views.generic import View
from django.db.models import Q
 
# 도서 목록 페이지
class books_list(View):
    def get(self,request):
        context = {}
        template_name = ""  
        # 전체 도서 불러오기
        books = Book.objects.all()

        page = int(request.GET.get('page', 1)) #페이지값 받아오기
        search_input = request.GET.get('search_input', '') #검색어 받아오기
        search_type = request.GET.get('search_type', '') #검색 유형 받아오기
        # ajax로 통신 : 페이지네이션 또는 검색
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': 
            template_name = 'books_table.html'
            if search_input: #검색어가 있을 경우 - 해당 검색어로 필터링
                if search_type == '전체':
                    books = Book.objects.filter(Q(title__icontains = search_input) | Q(author__icontains = search_input) | Q(publisher__icontains = search_input))
                elif search_type == '제목':
                    books =  Book.objects.filter(Q(title__icontains = search_input))
                elif search_type == '작가':
                    books =  Book.objects.filter(Q(author__icontains = search_input))
                elif search_type == '출판사':
                    books =  Book.objects.filter(Q(publisher__icontains = search_input))
        # GET 통신 : 페이지 불러오가
        else:            
            template_name = 'books_list.html'

        # 페이지네이션에 따라 10개씩 출력
        paginator = Paginator(books, 10)
        # 페이지 선택
        books_list = paginator.get_page(page)
        context = {"books_list":books_list,"search_input":search_input,"search_type":search_type}
        return render(request, template_name,context)

    def post(self,request):
        return redirect("books:list")

# 도서 상세 페이지
class books_detail(View):
    def get(self,request):
        context={}
        template_name = 'books_detail.html' 
        
        # 도서 isbn13 받아오기
        isbn13 = request.GET.get('isbn13', '') 

        if Book.objects.filter(isbn13 = isbn13).exists(): 
            book = Book.objects.get(isbn13 = isbn13) # 도서 객채 추가
            context["book"] = book


            # 도서 관련 리뷰가 있을 경우 추가
            reviews =  Review.objects.filter(book = book)[:3]
            if reviews.exists():
                context["reviews"] = reviews

            # 도서 관련 토론이 있을 경우 추가
            debates =  Debate.objects.filter(book = book)[:3]
            if debates.exists():
                context["debates"] = debates

            return render(request, template_name ,context)
        else:
            # 도서를 찾을 수 없습니다!
            return redirect("books:list")

    def post(self,request):
        return redirect("books:list")