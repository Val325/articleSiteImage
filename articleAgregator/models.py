from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
    images = models.ImageField(upload_to='images/') 
