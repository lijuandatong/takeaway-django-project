from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username



    def __str__(self):
        return self.first_name
