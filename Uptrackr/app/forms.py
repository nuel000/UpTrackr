from django import forms


class UserInputForm(forms.Form):
    email = forms.EmailField(label='Enter your email address')
    rss_url = forms.URLField(label='Enter your Upwork RSS URL')


class UserSignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')
    full_name = forms.CharField(label='Full Name', max_length=100)
    country = forms.CharField(label='Country', max_length=50)

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

