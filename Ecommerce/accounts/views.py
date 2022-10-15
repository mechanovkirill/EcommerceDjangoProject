from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# verification email
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

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

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account.'
            message = render_to_string('accounts/account_verification_message.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email) # for use if/else in login.html template

    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)

        user = auth.authenticate(email=email, password=password) # https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.authenticate
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'invalid login or password')
            return redirect('accounts:login-view')

    return render(request, 'accounts/login.html')


@login_required(login_url='accounts:login-view')
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('accounts:login-view')


def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # decode uidb64 get by url request and 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congraulations! Your account is activated.')
        return redirect('accounts:login-view')
    else:
        messages.error(request, 'Invalid activation link')
