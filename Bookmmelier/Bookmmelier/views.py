from django.shortcuts import render
from django.contrib import auth
from django.views.generic import View

# Create your views here.
class homeView(View):
    def get(self,request):
        return render(request, 'home.html')