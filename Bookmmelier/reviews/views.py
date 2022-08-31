from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.

class reviewsView(View):
    def get(self,request):
        reviews_list = Review.objects.all()
        page = int(request.GET.get('page', 1))
        search = request.GET.get('search', '')
        if search:  
            type = request.GET.get('type', '')
            if type == '전체':
                search_reviews = Review.objects.filter(
                    Q(title__icontains = search) | 
                    Q(user__icontains = search) | 
                    Q(contents__icontains = search)
                )
            elif type == '도서':
                search_reviews =  Book.objects.filter(Q(title__icontains = search))
            elif type == '작성자':
                search_reviews =  Book.objects.filter(Q(user__icontains = search))
            elif type == '내용':
                search_reviews =  Book.objects.filter(Q(contents__icontains = search))
            paginator = Paginator(search_reviews, 10)
            reviews_list = paginator.get_page(page)
            return render(request, 'reviews.html',{"reviews_list":reviews_list,"search":search,"type":type})
        else:            
            paginator = Paginator(Review.objects.all(), 10)                
            reviews_list = paginator.get_page(page)
            return render(request, 'reviews.html',{"reviews_list":reviews_list})

    def post(self,request):
        return None


class reviewswriteView(View):
    def get(self,request):
        if request.user.is_authenticated:
            paginator = Paginator(Book.objects.all(), 10)                
            books_list = paginator.get_page(1)
            return render(request, 'review_write.html',{"books_list":books_list})
        else:
            return redirect('/login')   
    def post(self,request):
        return None

def searchBooks(request):
    books = Book.objects.all()
    page = int(request.GET.get('page', 1)) #페이지값 받아오기
    search_input = request.GET.get('search_input', '') #검색어 받아오기
    search_type = request.GET.get('search_type', '')
    print("page:",page," search_input:",search_input," search_type:",search_type)

    if request.is_ajax(): #ajax로 통신 -> 페이지 또는 검색
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
        paginator = Paginator(books, 10)
        books_list = paginator.get_page(page)
        return render(request, 'books_search_table.html',{"books_list":books_list,"search_input":search_input,"search_type":search_type})
    else:
        return None




