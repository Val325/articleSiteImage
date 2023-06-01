from django import forms
 
class send_article_form(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,'cols': 20}))
    author = forms.CharField()

