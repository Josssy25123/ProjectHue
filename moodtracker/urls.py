from django.urls import path
from django.contrib.auth import views as auth_views
from .views import custom_logout
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main page
    path('register/', views.register, name='register'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]
