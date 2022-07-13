from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name ='signup'),
    path('login/', views.loginuser, name='login'),
    path('index/', views.index, name= 'index'),
    path('deposit/', views.deposit_view, name = 'deposit'),
    path('withrawal/', views.withdrawal_view, name = 'withdrawal'),
    path('transfer/', views.transfer_view, name = 'transfer'),
    path('logout/', views.logoutuser, name = 'logoutuser'),
]