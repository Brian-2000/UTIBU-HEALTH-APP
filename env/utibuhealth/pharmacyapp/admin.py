from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Order, Medication, Statement

# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Medication)
admin.site.register(Statement)
