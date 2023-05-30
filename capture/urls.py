from django.urls import path
from .views import home, read_tweets, download_tweets_file

app_name = 'capture'
urlpatterns = [
    path('', home, name='home'),
    path('read/', read_tweets, name='read_tweets'),
    path('download-tweets/<str:country_name>/', download_tweets_file, name='download_tweets_file')
]