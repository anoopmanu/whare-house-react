from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    user_type = models.CharField(default=1, max_length=10)

class Usermember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    age = models.IntegerField( null=True)
    number = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    image = models.ImageField(blank=True, upload_to="image/", null=True)


# Create your models here.

