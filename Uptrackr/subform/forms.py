from django import forms

class UserInputForm(forms.Form):
    email = forms.EmailField(label='Enter your email address')
    rss_url = forms.URLField(label='Enter your Upwork RSS URL')

