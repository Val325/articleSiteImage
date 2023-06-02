from django.db import models
 
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
    images = models.ImageField(upload_to='images/') 
