from django.urls import path
from .views import input_form

urlpatterns = [
    path('dashboard/', input_form, name='input_form'),
]
