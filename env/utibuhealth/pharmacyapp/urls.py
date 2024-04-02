from django.urls import path, include
from . import views

app_name = "pharmacyapp"

urlpatterns = [
    path("", views.loginview, name="login"),
    path("register/", views.register, name="register"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("patient_dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("medication/", views.medication, name="medication"),
    path("place_order/", views.place_order, name="place_order"),
    path("process_order/", views.process_order, name="process_order"),
    path("my_orders/", views.orders, name="my_orders"),
    path("all_patients/", views.lis_of_patients, name="all_patients"),
    path("admin_orders/", views.admin_orders, name="admin_orders"),
    
]