from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from rest_framework import status
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


from concurrent.futures import ThreadPoolExecutor
import subprocess

def run_main_script(email, rss_url):
    try:
        subprocess.run(["python", "main/main.py", email, rss_url], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running main.py:", e)


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


# Registration endpoint, this should register a user and save their details to the database
def sign_up(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            country = form.cleaned_data['country']
            password = form.cleaned_data['password']

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.full_name = full_name
            user.save()
            return render(request, 'signup_success.html')
        else:
            messages.error(request, 'One or more field(s) is empty!')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# This login endpoint is used to test if the dashboard will be... 
# ... shown to users upon successful login 
def log_in(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # Redirect to homepage upon successful login
                return redirect('success')
            else:
                # Handle invalid login credentials
                messages.error(request, 'Invalid email or password!')
                #form.add_error(None, 'Invalid login credentials')
        else:
            messages.error(request, 'Form error!')
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


def reset_password(request):
    if request.method == 'POST':
        form = ResetAccountForm(request.POST)

        if form.is_valid():
            # Change user password
            new_password = form.cleaned_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()

            # Update the session to maintain login
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Your password has been reset successfully!')
            return redirect('reset_password')  # Redirect to the same page after reset
    else:
        form = ResetAccountForm()

    return render(request, 'reset_password.html', {'form': form})


#-----------------------------Testing ----------------------------------------------------------------------#

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

@login_required
def alert_page(request):
    print("View accessed.")
    return render(request, 'alert.html')

def success(request):
    return render(request, 'login_success.html')





