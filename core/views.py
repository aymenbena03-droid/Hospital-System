from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment, Patient
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import PatientRegistrationForm

# Create your views here.

def home(request):
    doctors = Doctor.objects.all()
    
    return render(request, 'core/home.html', {'doctors': doctors})


# Booking an appointment
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        
        if date_str and time_slot:
            patient = Patient.objects.first()
            
            # Try Block to handle IntegrityError for duplicate appointments
            try:
                Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    date=date_str,
                    time_slot=time_slot,
                    status='Pending'
                )
                messages.success(request, 'Appointment booked successfully!')
                return redirect('home')
            # Catch the IntegrityError and display an error message
            except IntegrityError:
                messages.error(request, 'An appointment for this time slot already exists.')
                return redirect('book_appointment', doctor_id=doctor.id)
    
    return render(request, 'core/book_appointment.html', {'doctor': doctor})


def register_view(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to MediCare.")
            return redirect('home')
    else:
        form = PatientRegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome Back, {username}")
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
            