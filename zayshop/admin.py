from django.contrib import admin
from .models import Food, Drink, Profile, CartItemDrink, CartItemFood

admin.site.register(Food)
admin.site.register(Drink)
admin.site.register(Profile)
admin.site.register(CartItemDrink)
admin.site.register(CartItemFood)