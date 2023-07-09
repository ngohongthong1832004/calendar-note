from calendarSite.views import *
from django.urls import path

urlpatterns = [
    path('login/', login, name='login'),
    path("register/", register, name="register"),
    path('', index, name='index'),
]