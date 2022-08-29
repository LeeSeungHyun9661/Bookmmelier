from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q
# Create your views here.

class reviewsView(View):
    def get(self,request):
        return None

    def post(self,request):
        return None
