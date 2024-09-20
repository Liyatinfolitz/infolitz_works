from django.db import models

# Create your models here.


class LoginForm(models.Model):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=100, null=True)
