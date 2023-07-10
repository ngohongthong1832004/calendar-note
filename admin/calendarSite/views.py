from datetime import datetime, date
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import *


class CustomPagination(Paginator):
    def __init__(self, object_list, per_page, orphans=0,allow_empty_first_page=True, request=None, **kwargs):
        self.request = request
        super().__init__(object_list, per_page, orphans=orphans,allow_empty_first_page=allow_empty_first_page, **kwargs)
        

class RegisterView(View):
    def get(self, request):
        template_name = 'register.html'
        context = {
            # Add any required context data for your React components
        }
        return render(request, template_name, context)
    def post(self, request):
        (first_name , gmail, password, confirm) = (request.POST.get('first_name'), request.POST.get('gmail'), request.POST.get('password'), request.POST.get('confirm-password'))
        if User.objects.filter(username=gmail).exists():
            return HttpResponseRedirect("/register/")
        print(first_name, gmail, password, confirm)
        if password == confirm:
            user = User.objects.create_user(username=gmail, email=gmail, password=password, first_name=first_name)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            return HttpResponseRedirect("/register/")

class LoginView(View):
    def get(self, request):
        template_name = 'login.html'
        context = {
            # Add any required context data for your React components
        }
        return render(request, template_name, context)
    def post(self, request):
        (gmail, password) = (request.POST.get('gmail'), request.POST.get('password'))
        user = authenticate(request, username=gmail, password=password)
        if user is not datetime.now().strftime("%H:%M:%S.%f")[:-3]:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/login/")

class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")

class ForgotView(View):
    def get(self, request):
        template_name = 'forgot.html'
        context = {
            # Add any required context data for your React components
        }
        return render(request, template_name, context)
    def post(self, request):
        gmail = request.POST.get('gmail')
        if User.objects.filter(username=gmail).exists():
            user = User.objects.get(username=gmail)
            user.set_password(request.POST.get('password'))
            user.save()

class Index(LoginRequiredMixin, TemplateView):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    context_object_name = 'note'
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(user=self.request.user)[::-1]
        context['user'] = self.request.user.username
        print(context['notes'])
        return context
    
class AddNoteView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    def post(self, request):
        content = request.POST.get('content')
        date_ = request.POST.get('date')
        if date_ == "":
            date_ = str(date.today().strftime('%Y-%m-%d'))
        time = request.POST.get('time')
        if time == "":
            time = str(datetime.now().strftime("%H:%M"))
        alert = request.POST.get('alert', False)
        print(type(date_))
        note = Note.objects.create(user=request.user, content=content, date=date_, time=time, alert=alert)
        note.save()
        return HttpResponseRedirect("/")

class DeleteNoteView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        note = Note.objects.get(id=id)
        note.delete()
        return HttpResponseRedirect("/")

class EditNoteView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        content = request.POST.get('content')
        date_ = request.POST.get('date')
        if date_ == "":
            date_ = str(date.today().strftime('%Y-%m-%d'))
        time = request.POST.get('time')
        if time == "":
            time = str(datetime.now().strftime("%H:%M"))
        alert = request.POST.get('alert', False)
        print(content, date, time, alert)
        note = Note.objects.get(id=id)
        note.content = content
        note.date = date_
        note.time = time
        note.alert = alert
        note.save()
        return HttpResponseRedirect("/")
    
class ChangeAlertView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        note = Note.objects.get(id=id)
        print(note.alert)
        if note.alert == True:
            print("hai")
            alert = False
        else:
            print("hello")
            alert = True
        print(alert)
        note.alert = alert
        note.save()
        return HttpResponseRedirect("/")
