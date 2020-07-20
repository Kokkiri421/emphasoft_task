
from django.urls import path
from . import views

app_name = 'vk_oauth'
urlpatterns = [

    path('', views.index, name='index'),
]

