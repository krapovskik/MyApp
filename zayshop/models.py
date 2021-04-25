from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    food_name = models.CharField(max_length=250, blank=False)
    food_price = models.IntegerField(blank=False)
    food_details = models.CharField(max_length=1000, blank=False, default='')
    food_photo = models.FileField(default=False)

    def __str__(self):
        return self.food_name


class Drink(models.Model):
    drink_name = models.CharField(max_length=250, blank=False)
    drink_price = models.IntegerField(blank=False)
    drink_photo = models.FileField(default=False)

    def __str__(self):
        return self.drink_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=False)
    phonenumber = models.CharField(max_length=12, blank=False)
    birthdate = models.DateField(blank=False)
    facebook = models.CharField(max_length=1000)
    instagram = models.CharField(max_length=1000)
    profile_picture = models.FileField(default=False)

    def sum(self):
        return sum([item.price for item in self.user.cartitem_set.all()])

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    details = models.CharField(max_length=1000, null=True)
    photo = models.FileField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
