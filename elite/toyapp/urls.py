from django.urls import path,include
from toyapp import views


urlpatterns = [
    path("",views.index,name='toyapp'),
    path("register",views.register,name='registerU'),
    path("login",views.login,name='loginU'),
    path("user",views.user,name='User'),
    path('msg',views.msg,name='Msg')
]
