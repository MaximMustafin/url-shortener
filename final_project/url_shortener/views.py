from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.


def index(request):
    return render(request=request, template_name='url_shortener/index.html')


def all_links(request):
    return render(request=request, template_name='url_shortener/all_links.html')