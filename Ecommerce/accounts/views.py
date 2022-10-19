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

import requests
from carts.models import Cart, CartItem
from carts.views import get_cart_id

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

        user = auth.authenticate(email=email, password=password) # https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.authenticate
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=get_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    id_list = []
                    existing_variation_list = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        existing_variation_list.append(list(existing_variation))
                        id_list.append(item.id)

                    for pr in product_variation:
                        if pr in existing_variation_list:
                            index = existing_variation_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, f'Welcome {user.first_name} to our store! We wish you a good time')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                return redirect(nextPage)
            except:
                pass

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

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password.'
            message = render_to_string('accounts/reset_password_message.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('accounts:login-view')

        else:
            messages.error(request, 'Account does not exist. Please enter your account email.')
            return redirect('accounts:forgot-password-view')
    return render(request, 'accounts/forgot_password.html')

def password_validate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(
            uidb64).decode()  # decode uidb64 get by url request and 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('accounts:reset-password-view')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('accounts:login-view')


def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('accounts:login-view')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('accounts:reset-password-view')
    else:
        return render(request, 'accounts/resetPassword.html')