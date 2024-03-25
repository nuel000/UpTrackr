from django.urls import path
from .views import sign_up
from .views import log_in
from .views import log_out
from .views import update_account
from .views import input_form
from .views import UserListAPIView
from .views import base_2_view, home_page, base_view, reset_password, success_page, pricing_page,sigup_sucess_page, activate_account,resend_activation_mail,password_reset_request,password_reset_confirm

urlpatterns = [
    path('signup', sign_up, name='signup'),
    path('users', UserListAPIView.as_view(), name='user-list'),
    path('login', log_in, name='login'),
    path('alert', input_form, name='dashboard'),
    path('base', base_view, name='base'),
    path('', home_page, name='home'),
    path('base2', base_2_view, name='base2'),
    path('reset_password', reset_password, name='reset_password'),
    path('success', success_page, name='success'),
    path('pricing', pricing_page, name='pricing'),
    path('logout', log_out, name='logout'),
    #path('alert', alert_page, name='alert'),
    path('update_account', update_account, name='update_account'),
    path('signup_successful', sigup_sucess_page, name='signup_successful'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('resend_activation', resend_activation_mail, name='resend_activation_mail'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),

    

    
]
