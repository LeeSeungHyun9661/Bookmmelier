from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q

class booksView(View):
    def get(self,request):
        print("GET")
        books = Book.objects.all()
        page = int(request.GET.get('page', 1)) #페이지값 받아오기
        search_input = request.GET.get('search_input', '') #검색어 받아오기
        search_type = request.GET.get('search_type', '')

        print("page:",page," search_input:",search_input," search_type:",search_type)

        if request.is_ajax(): #ajax로 통신 -> 페이지 또는 검색
            print("ajax 통신")
            if search_input: #검색어가 있을 경우 - 해당 검색어로 필터링
                print("검색어 입력됨 : " + search_input)
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
            return render(request, 'books_table.html',{"books_list":books_list,"search_input":search_input,"search_type":search_type})
        else:
            print("get 통신")
            paginator = Paginator(books, 10)  
            books_list = paginator.get_page(page)
            return render(request, 'books.html',{"books_list":books_list})

    def post(self,request):
        print("POST")
        return None



class booksdetailView(View):
    def get(self,request):
        isbn13 = request.GET.get('isbn13', '')
        if Book.objects.filter(isbn13 = isbn13).exists():
            book = Book.objects.get(isbn13 = isbn13)
            return render(request, 'book_detail.html',{"book":book})
    def post(self,request):
        return None

# 좋아요
def likes(request,isbn13):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=isbn13)
        if book.like_users.filter(pk=request.user.pk).exists():
            book.like_users.remove(request.user.id)
            print('unlike!')
        else:
            print(request.user.id)
            book.like_users.add(request.user.id)
            print('like!')
            return redirect('/')
    return redirect('/login')
