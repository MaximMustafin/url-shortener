from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from . import utils

# Create your views here.

# view for rendering home page
def index(request):
    return render(request=request, template_name='url_shortener/index.html')


# view for rendering all links page
def all_links(request):
    return render(request=request, template_name='url_shortener/all_links.html')


# view for creating new short urls
def create_short_url(request):

    # get input full url from user's request
    full_url = request.POST['input-url']
    
    # check if input has url format
    if utils.is_valid_url(full_url):

        # return render of index page with short url
        return render(request=request, template_name='url_shortener/index.html', 
            context={'short_url': full_url})
    else:
        error_message = 'Input full URL`s format is wrong. Please try again...'

        # return render of index page with error_message
        return render(request=request, template_name='url_shortener/index.html', 
            context={'error_message': error_message})