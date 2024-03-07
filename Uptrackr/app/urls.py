from django.urls import path
from .views import sign_up,log_in,input_form,base_view,home_page,base_2_view,reset_password,success_page,pricing_page
from .views import UserListAPIView

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
    # Other URL patterns
]
