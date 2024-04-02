from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, MedicationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Medication, Order, Statement
from django.contrib import messages
from datetime import datetime
from .routers import LegacyDatabaseRouter
# Create your views here.


def loginview(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.admin:
                login(request, user)
                return redirect('pharmacyapp:admin_dashboard')
            elif user is not None and user.patient:
                login(request, user)
                return redirect('pharmacyapp:patient_dashboard')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error Validating Form'
    return render(request=request, template_name="pharmacyapp/authapp/login.html", context={"form":form})


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created successfully'
            return redirect('pharmacyapp:login')
        else:
            msg = 'form is not valid'

    else:
        form = SignUpForm()

    return render(request=request, template_name="pharmacyapp/authapp/register.html", context={"form":form})


def admin_dashboard(request):
    return render(request=request, template_name="pharmacyapp/adminapp/admin_dashboard.html")


def patient_dashboard(request):
    return render(request=request, template_name="pharmacyapp/patientapp/patient_dashboard.html")


def medication(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medicationupload = form.save(commit=False)
            medicationupload.name = form.cleaned_data['name']
            medicationupload.description = form.cleaned_data['description']
            medicationupload.price = form.cleaned_data['price']
            medicationupload.stock_quantity = form.cleaned_data['stock_quantity']

            medicationupload.save()

    else:
        form = MedicationForm()
    return render(request=request, template_name="pharmacyapp/adminapp/medication.html", context={"form":form})


@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        medication_id = request.POST.get('medication_id')
        quantity = request.POST.get('quantity')
        pick_up_date = request.POST.get('pick_up_date')
        delivery_option = request.POST.get('delivery_option')

        # Get the logged-in user and customer
        user = request.user

        try:
            medication = Medication.objects.get(id=medication_id)
        except Medication.DoesNotExist:
            messages.error(request, 'Medication does not exist.')
            return redirect('pharmacyapp:order')

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer")
        except ValueError:
            messages.error(request, 'Quantity must be a positive integer.')
            return redirect('pharmacyapp:order')

        if medication.stock_quantity < quantity:
            messages.error(request, 'Insufficient stock.')
            return redirect('pharmacyapp:place_order')

        # Convert pick_up_date string to a Date object
        if pick_up_date:
            try:
                pick_up_date = datetime.strptime(pick_up_date, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid pick-up date format.')
                return redirect('pharmacyapp:order')

        order = Order.objects.create(
            medication=medication,
            user=user,
            quantity=quantity,
            pick_up_date=pick_up_date,
            delivery_option=delivery_option
        )
        medication.stock_quantity -= quantity
        medication.save()

        messages.success(request, 'Order placed successfully.')
        return redirect('pharmacyapp:order')

    context = {
        'medications': Medication.objects.all(),
    }
    return render(request=request, template_name="pharmacyapp/patientapp/place_order.html", context=context)



@csrf_exempt
def get_statement(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    statements = Statement.objects.filter(customer=customer)

    statement_data = []
    for statement in statements:
        statement_data.append({
            'amount': statement.amount,
            'date': statement.date
        })

    return JsonResponse({'statements': statement_data})


def verify_stock_availability(order_items):
    """
    Check the stock availability of medications before confirming an order.
    """
    for item in order_items:
        try:
            medication = Medication.objects.get(id=item['medication_id'])
            if medication.stock_quantity < item['quantity']:
                return False
        except Medication.DoesNotExist:
            return False
    return True


def update_legacy_database(order_details):
    """
    Update the legacy database with new order details.
    """
    with connections['legacy_db'].cursor() as cursor:
        cursor.execute("INSERT INTO legacy_order_table (order_id, customer_name, total_amount) VALUES (%s, %s, %s)",
                       [order_details['order_id'], order_details['customer_name'], order_details['total_amount']])

def process_order(request):
    if request.method == 'POST':
        # Extract order items from the request
        order_items = [
            {
                'medication_id': int(request.POST.get('medication_id')),
                'quantity': int(request.POST.get('quantity'))
            }
        ]

        # Verify medication stock availability
        if not verify_stock_availability(order_items):
            messages.error(request, 'One or more medications are out of stock.')
            return redirect('order')

        # Create a new order instance and save it to the database
        total_amount = 0
        for item in order_items:
            medication = Medication.objects.get(id=item['medication_id'])
            order = Order.objects.create(
                medication=medication,
                quantity=item['quantity'],
                user=request.user  # Assuming the user is authenticated
            )
            total_amount += medication.price * item['quantity']

        # Update the legacy database with new order details
        order_details = {
            'order_id': order.id,  # Assuming order.id exists after creation
            'customer_name': request.user.username,  # Assuming user is authenticated
            'total_amount': total_amount
        }
        update_legacy_database(order_details)

        messages.success(request, 'Order placed successfully.')
        return redirect('order')

    # If request method is not POST or form validation fails, render the order page
    medications = Medication.objects.all()
    return render(request, 'pharmacyapp/adminapp/order.html', {'medications': medications})


def orders(request):
    order = Order.objects.filter(user=request.user)
    return render(request=request, template_name="pharmacyapp/patientapp/my_orders.html", context={"order":order})

def lis_of_patients(request):
    patients = User.objects.all()
    return render(request=request, template_name="pharmacyapp/adminapp/list_of_patients.html", context={"patients":patients})


def admin_orders(request):
    adminorders = Order.objects.all()
    return render(request=request, template_name="pharmacyapp/adminapp/all_orders.html", context={"adminorders":adminorders})
