from django.contrib import admin

# Register your models here.
from .models import Dish, Order

admin.site.register(Dish)
admin.site.register(Order)