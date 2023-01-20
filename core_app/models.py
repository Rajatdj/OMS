from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.company_name
    
class Token(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.token
