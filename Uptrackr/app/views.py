from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect
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
from .forms import UserLoginForm, UserSignupForm
from django.contrib.auth import authenticate, login

# Registration endpoint, this should register a user and save their details to the database
@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})

class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


def log_in(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                print("Logged in successfully")
                # Redirect to a success page or wherever you want
                return render(request, 'login.html', {'form': form})
                #return redirect('success_page')
            else:
                # Handle invalid login credentials
                print("Unsuccessful")
                form.add_error(None, 'Invalid login credentials')
    else:
        form = UserLoginForm()
        
    return render(request, 'login.html', {'form': form})
