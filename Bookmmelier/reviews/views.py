from urllib import request
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q
from reviews.forms import ReviewWriteFrom
from django.http import JsonResponse

# _____리뷰 리스트 및 검색 페이지_____
class reviews_list_View(View):    
    # 페이지 일반 접근
    def get(self,request): 
        # 전체 도서의 DB 연결
        reviews = Review.objects.all()
        #페이지 확인
        page = int(request.GET.get('page', 1))
        #입력된 검색어 확인
        search_input = request.GET.get('search_input', '') 
        #입력된 검색 유형 확인
        search_type = request.GET.get('search_type', '')

        #ajax로 통신 -> 페이지 또는 검색
        if request.is_ajax(): 
             #검색어가 있을 경우 검색어로 필터링
            if search_input:
                #검색어 구분에 따라 리뷰 데이터 필터링
                if search_type == '전체':
                    reviews = Review.objects.filter(
                        Q(book__title__icontains = search_input) | 
                        Q(user__name__icontains = search_input) | 
                        Q(contents__icontains = search_input)
                    )
                elif search_type == '도서':
                    reviews =  Review.objects.filter(Q(book__title__icontains = search_input))
                elif search_type == '작성자':
                    reviews =  Review.objects.filter(Q(user__name__icontains = search_input))
                elif search_type == '내용':
                    reviews =  Review.objects.filter(Q(contents__icontains = search_input))          

            #페이지네이션을 통해 10개씩 페이지로 정리
            paginator = Paginator(reviews, 10)
            #페이지 번호에 따라 페이지네이션 된 결과물 불러오기
            reviews_list = paginator.get_page(page)
            #결과 전송
            return render(request, 'reviews_table.html',{"reviews_list":reviews_list,"search_input":search_input,"search_type":search_type})
        else: #ajax로 통신 아님 -> 기본적인 페이지 접근
            paginator = Paginator(reviews, 10) 
            #페이지 번호에 따라 페이지네이션 된 결과물 불러오기 
            reviews_list = paginator.get_page(page)
            #결과 전송
            return render(request, 'reviews_list.html',{"reviews_list":reviews_list})            

    # 상단 메뉴바의 검색어 입력에 따른 검색의 결과를 반환함
    # 연결된 트리거는 Base.html에 포함되어 있음
    def post(self,request):
        # 전체 도서의 DB 연결
        reviews = Review.objects.all()
        #입력된 검색어 확인
        search_input = request.POST.get('review_search_input', '')         
        #입력된 검색 유형 확인
        search_type = request.POST.get('review_search_type', '') 

        # 필터링을 통한 도서 데이터 불러오기
        if search_type == '전체':
            reviews = Review.objects.filter(
                Q(title__icontains = search_input) | 
                Q(user__icontains = search_input) | 
                Q(contents__icontains = search_input)
            )
        elif search_type == '도서':
            reviews =  Review.objects.filter(Q(book__title__icontains = search_input))
        elif search_type == '작성자':
            reviews =  Review.objects.filter(Q(user__name__icontains = search_input))
        elif search_type == '내용':
            reviews =  Review.objects.filter(Q(contents__icontains = search_input)) 

        # 검색 결과에 따라 페이지를 불러옴
        paginator = Paginator(reviews, 10)
        reviews_list = paginator.get_page(1)
        return render(request, 'reviews_list.html',{"reviews_list":reviews_list,"search_input":search_input,"search_type":search_type})

# _____리뷰 작성 페이지_____
class reviews_write_View(View): 
    # 페이지 접근   
    def get(self,request):
        context={}
        #사용자가 현재 로그인중인지 확인
        if request.user.is_authenticated:
            #기본적인 도서 목록 데이터 호출
            paginator = Paginator(Book.objects.all(), 10)                
            books_list = paginator.get_page(1)
            context["books_list"] = books_list

            #리뷰 작성 폼 호출
            forms = ReviewWriteFrom()            
            context["forms"] = forms

            # 만약 사용자가 도서에서 서평 작성으로 넘어온 경우 도서가 이미 선택된 상태임
            isbn13 = request.GET.get('isbn13','')
            if isbn13:
                selected_book = Book.objects.get(isbn13 = isbn13)        
                context["selected_book"] = selected_book

            return render(request, 'review_write.html', context)
        else:
            return redirect('/login?next=' + request.path) 
    
    # 리뷰 작성 요청  
    def post(self,request):
        context={}
        # 응답 받은 별괄를 form으로 저장
        form = ReviewWriteFrom(request.POST)
        #isbn을 통해 현재 입력받은 도서의 isbn 확인
        isbn13 = request.POST.get('isbn13')
        # form을 통해 입력이 올바른지 먼저 확인
        if form.is_valid():  
            # 리뷰를 먼저 save
            review = form.save(commit=False)
            # 작성자의 정보를 현재 사용자와 연결
            review.user = request.user  
            # 리뷰의 도서를 isbn을 통해 검색한 도서 객체와 연결
            review.book = Book.objects.get(isbn13 = isbn13)
            #데이터베이스에 저장함
            review.save()
            # 작성된 리뷰 페이지로 이동
            context["review_id"] = review.review_id
            return JsonResponse(context)

# _____리뷰 수정 페이지_____
class review_update_View(View):
    # 페이지 접근
    def get(self,request):
        #사용자가 현재 로그인중인지 확인
        if request.user.is_authenticated:
            #기본적인 도서 목록 데이터 호출
            paginator = Paginator(Book.objects.all(), 10)                
            books_list = paginator.get_page(1)
            #현재 리뷰 페이지 아이디 불러오기
            review_id = request.GET.get('review_id', '')
            #현재 존재하는 리뷰인지 확인
            if Review.objects.filter(review_id = review_id).exists():
                review = Review.objects.get(review_id = review_id) 
                #리뷰의 작성자가 현재 로그인중인 작성자와 동일한지 확인
                if review.user == request.user: 
                    #리뷰 폼에 받은 정보를 담아서 폼에 저장
                    forms = ReviewWriteFrom(instance=review)
                    return render(request, 'review_update.html',{"books_list":books_list,"forms":forms,"review_id":review.review_id,"selected_book":review.book})
        else:
            return redirect('/login?next=' + request.path)   

    # 리뷰 수정 요청
    def post(self,request):
        # 응답 받은 결과를 form으로 저장
        form = ReviewWriteFrom(request.POST)
        # isbn을 통해 현재 입력받은 도서의 isbn 확인
        isbn13 = request.POST.get('isbn13')
        # 수정 리뷰의 아이디 확인
        review_id = request.POST.get('review_id')    
        # 현재 수정중인 리뷰가 존재하는지 확인
        if Review.objects.filter(review_id = review_id).exists():
            review = Review.objects.get(review_id = review_id)
            # 폼의 정보가 적절한지 확인
            if form.is_valid():
                review.title = form.title
                review.contents = form.contents
                review.rate = form.rate
                review.is_shared = form.is_shared
                # 도서가 갱신된 상태라면 반영
                review.book = Book.objects.get(isbn13 = isbn13)
                # 리뷰 데이터를 업데이트함
                review.save(force_update=True)
                return JsonResponse({"review_id":review_id})

# _____리뷰 상세보기 페이지_____
class review_detail_View(View):
    def get(self,request):
        context = {}
    # 리뷰 아이디를 통해 리뷰 데이터를 불러와 페이지에 전송
        review_id = request.GET.get('review_id', '')
        if Review.objects.filter(review_id = review_id).exists():
            review = Review.objects.get(review_id = review_id)
            context['review'] = review

            comments = Comment.objects.filter(review_id = review.review_id) 
            paginator = Paginator(comments, 5)
            comments_list = paginator.get_page(1)  
            context['comments_list'] = comments_list
            return render(request, 'review_detail.html',context)
    def post(self,request):
        context = {}
        if request.is_ajax(): #ajax로 통신 -> 페이지 또는 검색
            review_id = request.POST.get('review_id', '')
            page = request.POST.get('page', '')
            comments = Comment.objects.filter(review_id = review_id) 
            paginator = Paginator(comments, 5)
            comments_list = paginator.get_page(page)
            context['comments_list'] = comments_list
            return render(request, 'review_detail_comments.html',context)

# _____리뷰 작성 - 모달에서의 도서 선택_____
def review_write_modal_select_book(request):
    if request.is_ajax(): 
        isbn13 = request.POST.get('isbn13', '')
        selected_book = Book.objects.get(isbn13 = isbn13)
        return render(request, 'review_write_selected_book.html',{"selected_book":selected_book})

# _____리뷰 작성 - 모달에서의 도서 검색_____
def review_write_modal_search_Books(request):
    books = Book.objects.all()
    page = int(request.GET.get('page', 1)) #페이지값 받아오기
    search_input = request.GET.get('search_input', '') #검색어 받아오기
    search_type = request.GET.get('search_type', '')

    if request.is_ajax(): #ajax로 통신 -> 페이지 또는 검색        
        print("ajax 통신 확인")   
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
        return render(request, 'review_write_search_result.html',{"books_list":books_list,"search_input":search_input,"search_type":search_type})

# _____리뷰 삭제_____
def review_delete(request):
    review_id = request.GET.get('review_id', '')
    if Review.objects.filter(review_id = review_id).exists():
        review = Review.objects.get(review_id = review_id)
        if (review.user == request.user) or request.user.is_staff:
            review.delete()
            return redirect("/reviews")
    return None

# _____댓글 등록_____
def comment_upload(request):
    if request.is_ajax():
        context = {}
        comment_text = request.POST.get("comment_text")
        review = Review.objects.get(review_id = request.POST.get("review_id"))

        Comment.objects.create(review = review,contents = comment_text, user = request.user)
        comments = Comment.objects.filter(review = review) 
        paginator = Paginator(comments, 5)
        comments_list = paginator.get_page(1)  
        context['comments_list'] = comments_list
        return render(request, 'review_detail_comments.html',context)
# _____댓글 수정_____
def comment_update(request):
    if request.is_ajax():
        context = {}
        comment_text = request.POST.get("comment_text")
        comment_id = request.POST.get("comment_id")
       
        if Comment.objects.filter(comment_id = comment_id).exists():
            comment = Comment.objects.get(comment_id = comment_id)
            comment.contents = comment_text
            comment.save()
        
            review = Review.objects.get(review_id = request.POST.get("review_id"))
            comments = Comment.objects.filter(review = review) 

            paginator = Paginator(comments, 5)
            comments_list = paginator.get_page(1)  
            context['comments_list'] = comments_list 
            return render(request, 'review_detail_comments.html',context)

# _____댓글 삭제_____
def comment_delete(request):
    if request.is_ajax():
        context = {}
        comment_id = request.POST.get("comment_id")
       
        if Comment.objects.filter(comment_id = comment_id).exists():
            comment = Comment.objects.get(comment_id = comment_id)
            comment.delete()
        
            review = Review.objects.get(review_id = request.POST.get("review_id"))
            comments = Comment.objects.filter(review = review)  

            paginator = Paginator(comments, 5)
            comments_list = paginator.get_page(1)  
            context['comments_list'] = comments_list 

            return render(request, 'review_detail_comments.html',context)
        