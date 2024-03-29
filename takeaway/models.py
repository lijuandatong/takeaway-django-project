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
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.CharField(max_length=100)
    # "0"为下单未支付， ”1“为已支付+派送结束状态
    delivery_state = models.CharField(max_length=10)
    ordered = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    street = models.CharField(max_length=50, default="")
    zipcode = models.CharField(max_length=10, default="")
    email = models.EmailField(max_length=30, default="")
    phone = models.CharField(max_length=15, default="")

    def __str__(self):
        return str(self.order_id)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    payment = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=10)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.order.order_id)


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
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
    total_price = models.FloatField(max_length=20, default=0)
    total_discount = models.FloatField(max_length=20, default=0)

    def __str__(self):
        return str(self.cart.cart_id)


