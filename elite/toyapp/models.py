from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    mobile=models.CharField(max_length=20)

class UserDetails(models.Model):
    image=models.ImageField(null=True,blank=True,upload_to="static/")