from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.menu, name='menu'),
    path('home/new/', views.post_new, name='post_new'),
]