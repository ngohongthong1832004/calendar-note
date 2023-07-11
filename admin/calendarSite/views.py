from datetime import datetime, date
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
# from django.urls import reverse
from django.core.mail import send_mail
from django.db.models import Q
from django.conf import settings
from threading import Timer
from .models import *



# auto send alert 
def auto_send_alert():
    notes = Note.objects.filter(alert=True, date=str(date.today().strftime('%Y-%m-%d')))
    for note in notes:
        if note.time == str(datetime.now().strftime("%H:%M")):
            send_mail(
                'Alert from Calendar Note site',
                'You have a note: ' + note.content + 
                ' at ' + note.time +
                ' on ' + note.date ,
                settings.EMAIL_HOST_USER,
                [note.user.email],
                 
            )
            note.alert = False
            note.save()
    return None 


def run_interval():
    t = Timer(60.0, run_interval)
    t.start()
    auto_send_alert()

run_interval()

# Create your views here.


class VerifyView(View):
    def post(self, request, *args, **kwargs):
        gmail = request.POST.get('gmail')
        
        try:
            user = User.objects.get(username=gmail)
        except ObjectDoesNotExist:
            messages.error(request, "Gmail does not exist")
            return HttpResponseRedirect("/forgot/")
        
        send_mail(
            'Reset your password',
            'Click this link to reset your password: http://' + request.get_host() + '/change-password/'+user.email+'/',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return HttpResponseRedirect("/login/")
class ChangePass(TemplateView):
    template_name = 'changepass.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = kwargs.get('email')
        return context
    
class SaveChange(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('pass')
        newPass = request.POST.get('newPass')

        print(email, password, newPass)

        if password == newPass:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            messages.error(request, "Password and confirm password are not the same")
            return HttpResponseRedirect("/change-password/"+email+"/")

class RegisterView(View):
    def get(self, request):
        template_name = 'register.html'
        return render(request, template_name)
    def post(self, request):
        (first_name , gmail, password, confirm) = (request.POST.get('first_name'), request.POST.get('gmail'), request.POST.get('password'), request.POST.get('confirm-password'))
        if User.objects.filter(username=gmail).exists():
            messages.error(request, "Gmail already exists")
            return HttpResponseRedirect("/register/")
        print(first_name, gmail, password, confirm)
        if password == confirm:
            user = User.objects.create_user(username=gmail, email=gmail, password=password, first_name=first_name)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            messages.error(request, "Password and confirm password are not the same")
            return HttpResponseRedirect("/register/")

class LoginView(View):
    def get(self, request):
        template_name = 'login.html'
        return render(request, template_name)
    def post(self, request):
        (gmail, password) = (request.POST.get('gmail'), request.POST.get('password'))
        user = authenticate(request, username=gmail, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Gmail or password is incorrect")
            return HttpResponseRedirect("/login/")

class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")

class ForgotView(View):
    def get(self, request):
        template_name = 'forgot.html'
        return render(request, template_name)
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
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(user=self.request.user)[::-1]
        paginator = Paginator(context['notes'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['user'] = self.request.user.username
        context['current_link'] = ''
        context['page_obj'] = page_obj
        context['max_page'] = paginator.num_pages
        return context
    


class IndexFilterDate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    context_object_name = 'note'
    template_name = 'index.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(user=self.request.user).filter(date=self.kwargs['date'])
        paginator = Paginator(context['notes'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['user'] = self.request.user.username
        context['current_link'] = 'index-filter-date'
        context['page_obj'] = page_obj
        context['max_page'] = paginator.num_pages
        return context
    

class FilterDateView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    def post(self, request):
        date = request.POST.get('date')
        return HttpResponseRedirect("/index-filter-date/" + date)

class IndexFilterAlert(LoginRequiredMixin, TemplateView):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    context_object_name = 'note'
    template_name = 'index.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(user=self.request.user).filter(alert=True)
        paginator = Paginator(context['notes'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['user'] = self.request.user.username
        context['current_link'] = 'index-filter-alert'
        context['page_obj'] = page_obj
        context['max_page'] = paginator.num_pages
        return context

class IndexSearch(LoginRequiredMixin, TemplateView):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    context_object_name = 'note'
    template_name = 'index.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(user=self.request.user).filter(content__icontains=self.kwargs['search'].strip())
        paginator = Paginator(context['notes'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['user'] = self.request.user.username
        context['current_link'] = 'index-filter-search'
        context['page_obj'] = page_obj
        context['max_page'] = paginator.num_pages
        return context
class SearchNoteView (LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    def post(self, request):
        search = request.POST.get('search')
        return HttpResponseRedirect("/index-search/" + search)

class IndexOverdue(LoginRequiredMixin, TemplateView):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'redirect_to'  # Set the redirect field name
    context_object_name = 'note'
    template_name = 'index.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(user=self.request.user).filter(
            (Q(date__lte = str(date.today().strftime('%Y-%m-%d'))) & Q(time__lt=str(datetime.now().strftime("%H:%M")))))
        paginator = Paginator(context['notes'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['user'] = self.request.user.username
        context['current_link'] = 'index-overdue'
        context['page_obj'] = page_obj
        context['max_page'] = paginator.num_pages
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
