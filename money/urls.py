from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('new/', views.post_new, name='for_forms'),
    path('auth/', views.auth, name="auth"),
    path('signup/', views.SignUp.as_view(), name="signup"),
]