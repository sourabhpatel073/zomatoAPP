from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Dish(models.Model):
    dish_name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    availability=models.BooleanField(default=True)


class Order(models.Model):
    customer_name=models.CharField(max_length=200)
    dishes=models.ManyToManyField(Dish)
    STATUS_CHOICES=[
        ("received", "Received"),
        ("processing", "Processing"),
        ("served","Served"),
    ]    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='received')
    userNo=models.IntegerField(default=1)

class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Feedback(models.Model):
    REASON_CHOICES = [
    ('taste', 'Taste'),
    ('service', 'Service')
]
    RATING_CHOICES = [(i, i) for i in range(1, 6)] # 1 to 5 rating
    dishes = models.ManyToManyField(Dish)  # Assuming you have a Dish model
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)  # Making this optional
    reason = models.CharField(max_length=10, choices=REASON_CHOICES, default='taste')