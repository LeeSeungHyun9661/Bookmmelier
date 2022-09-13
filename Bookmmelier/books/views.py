from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Avg,Count,F
from reviews.models import Review
from .models import *
from django.views.generic import View
from django.db.models import Q
 
# 도서 목록 페이지
class booksView(View):    
    def get(self,request):
        # 전체 도서 불러오기
        books = Book.objects.all()
        page = int(request.GET.get('page', 1)) #페이지값 받아오기
        search_input = request.GET.get('search_input', '') #검색어 받아오기
        search_type = request.GET.get('search_type', '') #검색 유형 받아오기

        if request.is_ajax(): #ajax로 통신 -> 페이지 또는 검색
            template = 'books_table.html'
            if search_input: #검색어가 있을 경우 - 해당 검색어로 필터링
                if search_type == '전체':
                    books = Book.objects.filter(
                        Q(title__icontains = search_input) | 
                        Q(author__icontains = search_input) | 
                        Q(publisher__icontains = search_input)
                    )
                elif search_type == '제목':
                    books =  Book.objects.filter(Q(title__icontains = search_input))
                elif search_type == '작가':
                    books =  Book.objects.filter(Q(author__icontains = search_input))
                elif search_type == '출판사':
                    books =  Book.objects.filter(Q(publisher__icontains = search_input))
        else:            
            template = 'books_list.html'

        paginator = Paginator(books, 10)
        books_list = paginator.get_page(page)
        context = {"books_list":books_list,"search_input":search_input,"search_type":search_type}
        return render(request, template,context)

    def post(self,request):
        print("POST")
        return None

class booksdetailView(View):
    def get(self,request):
        context={}
        isbn13 = request.GET.get('isbn13', '')
        if Book.objects.filter(isbn13 = isbn13).exists():
            book = Book.objects.get(isbn13 = isbn13)
            context["book"] = book
            reviews =  Review.objects.filter(book = book)[:3]
            if reviews:
                context["reviews"] = reviews
            return render(request, 'book_detail.html',context)
    def post(self,request):
        return None

# 좋아요
def book_like(request):
    context = {}
    if request.is_ajax():
        id = request.POST.get("id")
        isbn13 = request.POST.get("isbn13")        
        book = Book.objects.get(isbn13 = isbn13)
        print(book.like_users.all)
        book.like_users.add(id)
        context["book"] = book

        return render(request, 'book_detail_like.html',context)

def book_dislike(request):
    context = {}
    if request.is_ajax():
        id = request.POST.get("id")
        isbn13 = request.POST.get("isbn13")        
        book = Book.objects.get(isbn13 = isbn13)
        book.like_users.remove(id)
        context["book"] = book
        return render(request, 'book_detail_like.html',context)