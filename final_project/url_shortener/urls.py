from django.urls import path
from . import views

app_name = 'url_shortener'

urlpatterns = [
    path('', views.index, name='index'),  # url for home page
    path('u/<str:short_url>', views.handle_short_url, name='handle'), # url for handling short urls from users
    path('allLinks', views.AllLinksView.as_view(), name='all_links'), # url for all links page
    path('myurl', views.create_short_url, name='create'), # url for creating new short urls
    path('delete/<int:short_url_id>', views.delete_short_url, name='delete'), # url for deleting short urls
]