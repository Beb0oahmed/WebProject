# models.py
from django.db import models

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    cover_photo = models.ImageField(upload_to='images/', null=True, blank=True)  # Add this line
    status = models.BooleanField(default='In Stock')  # Add the status field with default value

    def __str__(self):
        return self.title


class sign(models.Model):
    username = models.CharField(max_length=50) 
    last= models.CharField(max_length=50)
    password= models.CharField(max_length=50)
    email= models.CharField(max_length=50)
    user = models.BooleanField(default=True)
    admin = models.BooleanField(default=True)

    def str(self):
        return self.username
    
    
        