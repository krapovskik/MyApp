from django.contrib import admin
from .models import Food, Drink, Profile, CartItem

admin.site.register(Food)
admin.site.register(Drink)
admin.site.register(Profile)
admin.site.register(CartItem)
