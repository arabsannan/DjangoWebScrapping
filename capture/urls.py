from django.urls import path
from .views import home_view, read_view

app_name = 'capture'
urlpatterns = [
    path('', home_view, name='home'),
    path('read/', read_view, name='read')
]