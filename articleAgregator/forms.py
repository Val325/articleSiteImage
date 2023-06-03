from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class send_article_form(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,'cols': 20}))
    author = forms.CharField()
    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'file_upload'}))
    class Meta:
        model = Article 
        fields = ('text', 'author','images')
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']
        help_texts = {
            'username': None,
            'email': None
        }
