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
            return render(request, 'review_write.html')
        else:
            return redirect('/')     

    def post(self,request):
        return None

def searchBooks(request):
    context = {}
    page = int(request.GET.get('page', 1))
    search = request.GET.get('search_input', '')
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
        context = {"book_list":book_list,"search":search,"type":type}
    else:
        paginator = Paginator(Book.objects.all(), 10)                
        book_list = paginator.get_page(page)        
        context = {"book_list":book_list}
    print("context:",context)
    return render(request,'books_table.html',context)
    

