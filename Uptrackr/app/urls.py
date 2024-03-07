from django.urls import path
from .views import sign_up
from .views import log_in
from .views import log_out
from .views import input_form
from .views import update_account
from .views import reset_password
from .views import UserListAPIView

urlpatterns = [
    path('signup', sign_up, name='signup'),
    path('users', UserListAPIView.as_view(), name='user-list'),
    path('login', log_in, name='login'),
    path('logout', log_out, name='logout'),
    path('dashboard', input_form, name='dashboard'),
    path('update_account', update_account, name='update_account'),
    path('reset_password', reset_password, name='reset_password')
    
]
