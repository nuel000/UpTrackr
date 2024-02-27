from django.urls import path
from .views import sign_up
from .views import UserListAPIView

urlpatterns = [
    path('signup', sign_up, name='signup'),
    path('users', UserListAPIView.as_view(), name='user-list'),

]