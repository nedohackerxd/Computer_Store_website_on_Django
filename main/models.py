from django.db import models

class User(models.Model):
    name = models.CharField(max_length=25)
    products = models.TextField()

class Account(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=25)
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
        primary_key=True
    )