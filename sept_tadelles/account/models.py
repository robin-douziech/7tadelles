from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

'''
class ProfilePhoto(models.Model) :

    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.caption
'''

class User(AbstractUser):
    
    profile_photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, null=True, blank=True)
    password_reset_token = models.CharField(max_length=64, null=True, blank=True)

    discord_verified = models.BooleanField(default=False)
    discord_username = models.CharField(max_length=50, null=True, blank=True)
    discord_verification_token = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self) :
        return self.username
