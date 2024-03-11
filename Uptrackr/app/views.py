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
from .forms import UserInputForm, UserLoginForm, UserSignupForm, UpdateAccountForm, ResetAccountForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Import the User model (testing...
#... without creating an actual user)
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

# def sign_up(request):
#     if request.method == 'POST':
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # Redirect to the login page after successful registration
#             return redirect('login')  # Assuming the URL name for the login page is 'login'
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         form = UserSignupForm()
#     return render(request, 'signup.html', {'form': form})


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
            #user = CustomUser.objects.create_superuser(username, email, full_name, password, country)
            print('Redirected successfully')
            return redirect('login')
        else:
            print('Unsuccessful')
            print(form.errors)

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
        print('Inside first form')
        if form.is_valid():
            print('Form is Valid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                print("Successful Login")
                # Redirect to the dashboard upon successful login
                return redirect('home')
            else:
                # Handle invalid login credentials
                print("Unsuccessful 001")
                print(form.errors)
                form.add_error(None, 'Invalid login credentials')
        else:
            print("Unsuccessful 002")
            print(form.errors)
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
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
            request.user.password = form.cleaned_data.get('password', request.user.password)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.full_name = form.cleaned_data.get('full_name')
            request.user.country = form.cleaned_data.get('country')
            request.user.save()

            # If you're using the CustomUser model
            user = request.user
            user.full_name = full_name
            user.save()

            messages.success(request, 'Your account has been updated successfully!')
            return redirect('signup')  # Redirect to the same page after update
    else:
        form = UpdateAccountForm()

    return render(request, 'update_account.html', {'form': form})


@login_required
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

def alert_page(request):
    return render(request, 'alert.html')





