from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('new/', views.post_new, name='for_forms'),
    path('', views.auth, name="auth"),
    path('signup/', views.SignUp.as_view(), name="signup"),
]