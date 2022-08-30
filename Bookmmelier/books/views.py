from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q
# Create your views here.

class booksView(View):
    def get(self,request):
        page = int(request.GET.get('page', 1))
        search = request.GET.get('search', '')
        if search:         
            type = request.GET.get('type', '')
            if type == '전체':
                search_books = Book.objects.filter(
                    Q(title__icontains = search) | 
                    Q(author__icontains = search) | 
                    Q(publisher__icontains = search)
                )
            elif type == '제목':
                search_books =  Book.objects.filter(Q(title__icontains = search))
            elif type == '작가':
                search_books =  Book.objects.filter(Q(author__icontains = search))
            elif type == '출판사':
                search_books =  Book.objects.filter(Q(publisher__icontains = search))
            paginator = Paginator(search_books, 10)
            book_list = paginator.get_page(page)
            return render(request, 'books.html',{"book_list":book_list,"search":search,"type":type})
        else:
            paginator = Paginator(Book.objects.all(), 10)                
            book_list = paginator.get_page(page)
            return render(request, 'books.html',{"book_list":book_list})

    def post(self,request):
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
