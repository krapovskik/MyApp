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

    def sum_food(self):
        if self.user.cartitemfood_set.all().count() > 0:
            return sum(self.user.cartitemfood_set.all().values_list('food_price', flat=True))
        else:
            return 'KKK'

    def sum_drink(self):
        if self.user.cartitemdrink_set.all().count() > 0:
            return sum(self.user.cartitemdrink_set.all().values_list('drink_price', flat=True))
        else:
            return 0

    def __str__(self):
        return self.user.username

#
# class Item(models.Model):
#     name = models
#     price =
#     details =
#     photo =
#     category =


class CartItemDrink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink_id = models.IntegerField(blank=False)

    def __str__(self):
        return Drink.objects.get(id=self.drink_id).drink_name


class CartItemFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_id = models.IntegerField(blank=False)

    def __str__(self):
        return Food.objects.get(id=self.food_id).food_name



