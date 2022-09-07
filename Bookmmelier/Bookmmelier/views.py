from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.contrib import auth
from django.views.generic import View
from django.core.paginator import Paginator
from reviews.models import Review
from django.db.models import Q

# Create your views here.
class homeView(View):
    def get(self,request):
        return render(request, 'home.html')


def reviewsearch(request):
    print("search 도착")
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        page = int(request.POST.get('page', 1)) #페이지값 받아오기
        search_input = request.POST.get('search_input', '') #검색어 받아오기
        search_type = request.POST.get('search_type', '') #검색 유형 받아오기
        print(page,search_input,search_type)

        if search_type == '전체':
            search_reviews = Review.objects.filter(
                Q(title__icontains = search_input) | 
                Q(user__icontains = search_input) | 
                Q(contents__icontains = search_input)
            )
        elif search_type == '도서':
            search_reviews =  Review.objects.filter(Q(title__icontains = search_input))
        elif search_type == '작성자':
            search_reviews =  Review.objects.filter(Q(user__icontains = search_input))
        elif search_type == '내용':
            search_reviews =  Review.objects.filter(Q(contents__icontains = search_input))   

        paginator = Paginator(search_reviews, 10)
        reviews_list = paginator.get_page(page)

        return render(request, 'reviews.html',{"reviews_list":reviews_list,"search":search_input,"search_type":search_type})
