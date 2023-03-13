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


class Food(models.Model):
    ID_MAX_LENGTH = 30

    food_id = models.CharField(max_length=ID_MAX_LENGTH)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='food_images', blank=True)
    price = models.FloatField(max_length=20)
    discounted_price = models.FloatField(max_length=20)
    description = models.CharField(max_length=300)
    address = models.CharField(max_length=100)
    rating = models.FloatField(max_length=3)

    def __str__(self):
        return self.title


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash = models.FloatField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=30)
    food_ids = models.CharField(max_length=300)
    payment = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=10)

    def __str__(self):
        return self.id


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    back_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.cart.cart_id
