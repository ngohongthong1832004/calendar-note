from django.shortcuts import render


def login(request):
    template_name = 'login.html'
    context = {
        # Add any required context data for your React components
    }
    return render(request, template_name, context)


def register(request):
    template_name = 'register.html'
    context = {
        # Add any required context data for your React components
    }
    return render(request, template_name, context)

def index(request):
    template_name = 'index.html'
    context = {
        # Add any required context data for your React components
    }
    return render(request, template_name, context)