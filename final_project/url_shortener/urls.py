from django.urls import path
from . import views

app_name = 'url_shortener'

urlpatterns = [
    path('', views.index, name='index'),
    path('u/<str:short_url>', views.handle_short_url, name='handle'),
    path('allLinks', views.all_links, name='all_links'),
    path('myurl', views.create_short_url, name='create')
]