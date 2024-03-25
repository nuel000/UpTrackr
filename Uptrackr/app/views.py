from rest_framework.decorators import api_view, permission_classes
from django_countries import countries
from django.utils.encoding import force_str
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import CustomUser
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from main.reset_password import send_reset_password_mail
from django.contrib.auth.models import User
from main.send_activation_mail import send_activation_mail
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from rest_framework import generics
from .models import CustomUser
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from .forms import UserInputForm, UserLoginForm, UserSignupForm
from .forms import UpdateAccountForm, ResetAccountForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import subprocess

def run_main_script(email, rss_url):
    try:
        subprocess.run(["python", "main/main.py", email, rss_url], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running main.py:", e)

@login_required
def input_form(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            rss_url = form.cleaned_data['rss_url']   
            run_main_script(email, rss_url)
            return redirect('success')
    else:
        form = UserInputForm()
    return render(request, 'alert.html', {'form': form})

from django.contrib.auth.tokens import default_token_generator

def sign_up(request):
    countries_list = countries
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            password = form.cleaned_data['password']
            
            
            # Create user account with is_active=False
            try:
                user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
                user.first_name = full_name
                user.save()
            except IntegrityError:
                error_message = "Username already exists. Please choose a different username."
                return render(request, 'signup.html', {'message': error_message})            
            # Generate token for email verification
            token = default_token_generator.make_token(user) 
            current_domain = HttpRequest.get_host(request)
            activation_link = f'{request.scheme}://{current_domain}{reverse("activate", kwargs={"uidb64": urlsafe_base64_encode(force_bytes(user.pk)), "token": token})}'
            send_activation_mail(email, activation_link)
            # Redirect to a page indicating successful signup
            return render(request, 'signup_success.html')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'countries': countries_list, 'form': form})

def resend_activation_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Handle the case where the user with the provided email doesn't exist
            error_message = 'User with this email address does not exist.'
            return render(request, 'resend_activation_mail.html', {'error_message': error_message})
        except MultipleObjectsReturned:
            error_message = 'Multiple users found with this email address. Please contact support.'
            return render(request, 'resend_activation_mail.html', {'error_message': error_message})
        # Generate token for email verification
        token = default_token_generator.make_token(user)
        current_domain = request.get_host()
        activation_link = f'{request.scheme}://{current_domain}{reverse("activate", kwargs={"uidb64": urlsafe_base64_encode(force_bytes(user.pk)), "token": token})}'
        # Send activation email
        send_activation_mail(email, activation_link)
        # Display success message
        message = """Activation email has been sent successfully
                        """
        return render(request, 'resend_activation_mail.html',{'message':message})
    else:
        return render(request, 'resend_activation_mail.html')

       
def activate_account(request, uidb64, token):
    form = UserLoginForm()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        # Activate user account
        user.is_active = True
        user.save()
        return render(request, 'activation_successful.html')
    else:
        return render(request, 'login.html', {'message': "Unable to actiavte your account <a href='/resend_activation'>Click here to resend activation link</a>", 'form': form})

class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# This login endpoint is used to test if the dashboard will be... 
# ... shown to users upon successful login 
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            # Check password validity here and handle login accordingly
        except ObjectDoesNotExist:
            error_message = "User does not exist. Please register or check your credentials."
            return render(request, 'login.html', {'message': error_message})
        user = authenticate(request, username=username, password=password)
        user_check  =  User.objects.get(username=username)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to the home page
                return redirect('home')
        elif user is None and not user_check.is_active:
                # Account is not activated
                message = "Account not activated. <a href='/resend_activation'>Click here to resend activation link</a>"
                return render(request, 'login.html', {'message': message})
        elif user is None and user_check.is_active:
            # Invalid login credentials
            message = """Invalid login credentials. \n
                        """
            return render(request, 'login.html', {'message': message})
        elif user is None and user_check is None:
            comment = get_object_or_404(username=username)
            messages.error(request, 'User does not exist.')
          
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('login')


@login_required
def update_account(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST)

        if form.is_valid():
            # Update user information
            request.user.username = form.cleaned_data.get('username', request.user.username)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.full_name = form.cleaned_data.get('full_name')
            request.user.country = form.cleaned_data.get('country')

            # Update password only if it's provided in the form
            new_password = form.cleaned_data.get('password')
            if new_password:
                request.user.set_password(new_password)

            request.user.save()

            # Update the session with the new user details
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Your account has been updated successfully!')
            logout(request)  # Logout the user after updating
            return redirect('login')  # Redirect to the login page after update
    else:
        form = UpdateAccountForm()

    return render(request, 'update_account.html', {'form': form})

def password_reset_request(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Handle the case where the user with the provided email doesn't exist
            return render(request, 'reset_password.html', {'error_message': 'User with this email address does not exist.'})
        except MultipleObjectsReturned:
            error_message = 'Multiple users found with this email address. Please contact support.'
            return render(request, 'resend_activation_mail.html', {'error_message': error_message})
        
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))  # Encode the user's primary key
        reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        
        # Send password reset email
        send_reset_password_mail(email, reset_url)
        # Redirect to a page indicating that the password reset email has been sent
        return render(request, 'reset_password.html',{'message':'We have sent a reset link to your email. Please click on the link to reset your password.'})
    else:
        return render(request, 'reset_password.html')


def password_reset_confirm(request, uidb64, token):
    
    print("UIDb64:", uidb64)  # Add this line to log uidb64 value
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
    except Exception as e:
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
            message = 'Your password has been successfully reset. You can now login with your new password'
            return render(request, 'password_reset_confirm.html', {'message': message})
        else:
            # If request method is not POST, render the form without the message
            return render(request, 'password_reset_confirm.html')
    else:
        # Handle invalid or expired token
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('password_reset')    
    















#-----------------------------Testing ----------------------------------------------------------------------#
@login_required
def base_view(request):
    return render(request, 'base.html')

def base_2_view(request):
    return render(request, 'base_html_2.html')

def reset_password(request):
    return render(request, 'reset_password.html')

def home_page(request):
    return render(request, 'index.html')

def success_page(request):
    return render(request, 'success.html')

def pricing_page(request):
    return render(request, 'pricing.html')

def sigup_sucess_page(request):
    return render(request, 'signup_success.html')

# def pass_reset(request):
#     return render(request, 'password_reset_confirm.html')


#def alert_page(request):
    #print("View accessed.")
    #return render(request, 'alert.html')






