from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from rest_framework import generics
from .models import CustomUser
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from .forms import UserInputForm, UserLoginForm, UserSignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  
# Import the User model (testing...# #...without creating an actual user)

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
        print('Redirected successfully')
        return redirect('login')

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

            # For testing purposes, create a temporary user
            # I'll remove before production
            temp_user, created = User.objects.get_or_create(username=username)
            if created:
                temp_user.set_password(password)
                temp_user.save()

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                print("Successful Login")
                # Redirect to the dashboard upon successful login
                return redirect('dashboard')
            else:
                # Handle invalid login credentials
                print("Unsuccessful")
                form.add_error(None, 'Invalid login credentials')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


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




