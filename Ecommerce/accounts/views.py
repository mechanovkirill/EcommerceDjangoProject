from django.shortcuts import render
from .forms import RegistrationForm


# Create your views here.


def register_view(request):
    form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    return render(request, 'accounts/login.html')


def logout_view(request):
    return render(request, 'accounts/logout.html')
