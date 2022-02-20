from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('menu/new/', views.post_new, name='for_forms'),
    path('', views.auth, name="auth"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('menu/history/', views.history, name="history"),
    path('export_users_xls/', views.export_post_xls),
]