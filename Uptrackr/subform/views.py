from django.shortcuts import render, redirect
from .forms import UserInputForm
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
    else:
        form = UserInputForm()
    return render(request, 'input_form.html', {'form': form})
