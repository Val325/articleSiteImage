from django import forms
from .models import *

class send_article_form(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,'cols': 20}))
    author = forms.CharField()
    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'file_upload'}))
    class Meta:
        model = Article 
        fields = ('text', 'author','images') 
