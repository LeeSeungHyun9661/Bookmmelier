from django.shortcuts import render, redirect
from django.views.generic import View
from books.models import Book
from debates.forms import DebateCreateFrom
from debates.models import Debate, Message
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
# Create your views here.


class debates_list(View):
    def get(self,request):
        context = {}
        template_name = "debates_list.html"
        debates = Debate.objects.all()
        context["debates"] = debates
      
        paginator = Paginator(Book.objects.all(), 10)                
        books_list = paginator.get_page(1)
        context["books_list"] = books_list
        return render(request, template_name,context)

    def post(self,request):
        context = {}
        template_name = ""        
        return render(request, template_name,context)

class debates_create(View):
    def get(self,request):
        context = {}
        template_name = "debates_create.html"

        if request.user.is_authenticated:
            # 토론 생성 폼
            forms = DebateCreateFrom()
            context["forms"] = forms
            
            # 도서 목록 불러오기
            paginator = Paginator(Book.objects.all(), 10)                
            books_list = paginator.get_page(1)
            context["books_list"] = books_list

            isbn13 = request.GET.get('isbn13','')
            if isbn13:
                selected_book = Book.objects.get(isbn13 = isbn13)
                context["selected_book"] = selected_book
            return render(request, template_name,context)
        else:
            isbn13 = request.GET.get('isbn13','')
            return redirect('/login?next=' + request.path+ '?isbn13=' + isbn13) 

    # 토론 생성
    def post(self,request):
        # 응답 받은 별괄를 form으로 저장
        context = {}
        form = DebateCreateFrom(request.POST)
        #isbn을 통해 현재 입력받은 도서의 isbn 확인
        isbn13 = request.POST.get('isbn13')
        # form을 통해 입력이 올바른지 먼저 확인
        if form.is_valid():  
            # 리뷰를 먼저 save
            debate = form.save(commit=False)
            # 작성자의 정보를 현재 사용자와 연결
            debate.user = request.user  
            # 리뷰의 도서를 isbn을 통해 검색한 도서 객체와 연결
            debate.book = Book.objects.get(isbn13 = isbn13)
            #데이터베이스에 저장함
            debate.save()
            # 작성된 리뷰 페이지로 이동
            context["debate_id"] = debate.debate_id 
            return JsonResponse(context)

class debates_update(View):
    def get(self,request):
        context = {}
        template_name = "debates_update.html"
        if request.user.is_authenticated:
            # 도서 목록 불러오기
            paginator = Paginator(Book.objects.all(), 10)                
            books_list = paginator.get_page(1)
            context["books_list"] = books_list

            debate_id = request.GET.get('debate_id', '')
            #현재 존재하는 리뷰인지 확인
            if Debate.objects.filter(debate_id = debate_id).exists():
                debate = Debate.objects.get(debate_id = debate_id) 
                context["debate_id"] = debate.debate_id

                if debate.user == request.user: 
                    #리뷰 폼에 받은 정보를 담아서 폼에 저장
                    forms = DebateCreateFrom(instance=debate)
                    context["forms"] = forms
                    context["selected_book"] = debate.book                    
                    return render(request, template_name,context)
        else:
            return redirect('/login?next=' + request.path)
    
    def post(self,request):
        # 응답 받은 결과를 form으로 저장
        form = DebateCreateFrom(request.POST)
        # isbn을 통해 현재 입력받은 도서의 isbn 확인
        isbn13 = request.POST.get('isbn13')
        # 수정 리뷰의 아이디 확인
        debate_id = request.POST.get('debate_id')    
        # 현재 수정중인 리뷰가 존재하는지 확인
        if Debate.objects.filter(debate_id = debate_id).exists():
            debate = Debate.objects.get(debate_id = debate_id)
            # 폼의 정보가 적절한지 확인
            if form.is_valid():
                debate.title = form.title
                debate.subtitle = form.subtitle
                # 도서가 갱신된 상태라면 반영
                debate.book = Book.objects.get(isbn13 = isbn13)
                # 리뷰 데이터를 업데이트함
                debate.save(force_update=True)
                return JsonResponse({"debate_id":debate_id})

class debates_detail(View):
    messages = {}

    def get(self,request):
        context = {}
        # 토론방 정보 불러오기
        debate_id = request.GET.get('debate_id','')
        debate = Debate.objects.get(debate_id = debate_id)

        # 토론 페이지의 토론 불러오기
        if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            template_name = "debates_messages_item.html"

            debate_id = request.GET.get('debate_id','')
            page = int(request.GET.get('page',1))

            debate = Debate.objects.get(debate_id = debate_id)
            messages = Message.objects.filter(debate = debate).order_by('-time_created')
            
            #페이지네이션을 통해 10개씩 페이지로 정리
            paginator = Paginator(messages, 5)
            #페이지 번호에 따라 페이지네이션 된 결과물 불러오기
            messages_list = paginator.get_page(page)
        
            context["has_next"] = messages_list.has_next()
            context["length"] = len(messages_list)
            context["messages_list"] = reversed(messages_list)
            print("page:",page,"messages_list",messages_list)

            return render(request, template_name,context)
        # 토론 페이지 처음 접근 
        else:
            if debate:
                # 토론 방에 대한 정보 저장
                template_name = "debates_detail.html"
                context["debate"] = debate
                # 토론 방에 연결괸 메시지 불러오기
                self.messages = Message.objects.filter(debate = debate).order_by('-time_created')                
                return render(request, template_name,context)
        
    # 메시지 작성 기능
    def post(self,request):
        if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            print(request.POST)
            debate_id = request.POST.get('debate_id','')
            debate = Debate.objects.get(debate_id = debate_id)

            message = Message()
            message.debate = debate
            message.contents = request.POST.get('contents')
            message.user = request.user
            message.save()

            message = message.__dict__
            message.pop('_state')

            return JsonResponse(message, safe=False)   


# _____토론 목록 - 모달에서의 도서 선택_____
def debates_list_select_book(request):
    context = {}
    template_name = ""
    # ajax 통신
    if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': 
        template_name = 'debates_list_selected_book.html'

        isbn13 = request.POST.get('isbn13', '')
        selected_book = Book.objects.get(isbn13 = isbn13)
        context["selected_book"] = selected_book

        # 선택된 도서에 해당하는 토론 목록 불러오기
        debates = Debate.objects.filter(book = selected_book)
        if debates.exists():
            paginator = Paginator(debates, 10)                
            debates_list = paginator.get_page(1)
            context["debates_list"] = debates_list    
        return render(request, template_name,context)

# _____토론 생성 - 모달에서의 도서 선택_____
def debates_create_select_book(request):
    context = {}
    template_name = ""
    # ajax 통신
    if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': 
        template_name = 'debates_create_selected_book.html'

        isbn13 = request.POST.get('isbn13', '')
        selected_book = Book.objects.get(isbn13 = isbn13)
        context["selected_book"] = selected_book

        return render(request, template_name,context)


# _____토론 작성 - 모달에서의 도서 검색_____
def debates_list_search_Books(request):
    context = {}
    template_name = ""

    books = Book.objects.all()
    page = int(request.GET.get('page', 1)) #페이지값 받아오기
    search_input = request.GET.get('search_input', '') #검색어 받아오기
    search_type = request.GET.get('search_type', '')

    if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': #ajax로 통신 -> 페이지 또는 검색 

        template_name = 'debates_list_search_result.html'
        context["search_input"] = search_input
        context["search_type"] = search_type

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

        context["books_list"] = books_list
        
        return render(request, template_name,context)

def debates_delete_message(request):
    if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        message_id = request.POST.get("message_id")

        if Message.objects.filter(message_id = message_id).exists():
            message = Message.objects.get(message_id = message_id)
            message.delete()
            return HttpResponse("OK")

def debates_update_message(request):
    if  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        message_text = request.POST.get("message_text")
        message_id = request.POST.get("message_id")

        if Message.objects.filter(message_id = message_id).exists():
            message = Message.objects.get(message_id = message_id)
            message.contents = message_text
            message.save()
            return HttpResponse("OK")
    return HttpResponse("False")

def debates_delete(request):
    debate_id = request.GET.get('debate_id', '')
    if Debate.objects.filter(debate_id = debate_id).exists():
        debate = Debate.objects.get(debate_id = debate_id)
        if debate.user == request.user :
            debate.delete()
            return redirect("/debates")
    return None
