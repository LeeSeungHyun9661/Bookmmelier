from django.shortcuts import render
from django.views.generic import View
from debates.models import Debate
# Create your views here.


class debates_list(View):
    def get(request):
        context = {}
        template_name = "debates_list.html"

        debates = Debate.object.all()
        context["debates"] = debates

        return render(request, template_name,context)
    def post(request):
        context = {}
        template_name = ""        
        return render(request, template_name,context)

class debates_create(View):
    def get(request):
        context = {}
        template_name = ""
        return render(request, template_name,context)
    def post(request):
        context = {}
        template_name = ""        
        return render(request, template_name,context)

class debates_detail(View):
    def get(request):
        context = {}
        template_name = ""
        return render(request, template_name,context)
    def post(request):
        context = {}
        template_name = ""        
        return render(request, template_name,context)


def debates_upload_message(request):
    context = {}
    template_name = ""
    return render(request, template_name,context)

def debates_delete_message(request):
    context = {}
    template_name = ""
    return render(request, template_name,context)

def debates_update_message(request):
    context = {}
    template_name = ""
    return render(request, template_name,context)