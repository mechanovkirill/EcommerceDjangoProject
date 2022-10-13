from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password
            )
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    return render(request, 'accounts/login.html')


def logout_view(request):
    return render(request, 'accounts/logout.html')
