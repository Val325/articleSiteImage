from django.db import models
 
class Article(models.Model):
    text = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
 
