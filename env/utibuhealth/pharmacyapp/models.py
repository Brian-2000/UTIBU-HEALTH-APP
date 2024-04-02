from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    admin = models.BooleanField('Admin', default=False)
    patient = models.BooleanField('Patient', default=False)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order", null=True, blank=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    pick_up_date = models.DateTimeField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    delivery_option = models.CharField(max_length=100, choices=[('pharmacy_pickup', 'Pharmacy Pickup'),
                                                               ('home_delivery', 'Home Delivery')])

    def __str__(self):
        return f"{self.user} - {self.medication} - {self.order_date}"

class Statement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.customer} - {self.amount} - {self.date}"
