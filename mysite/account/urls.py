from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.index, name = "account_status"),
    path('signup/', views.signup, name ='signup'),
    path('login/', views.loginuser, name='login'),
    path('login/account/currentusser', views.index, name= 'currentusser'),
]