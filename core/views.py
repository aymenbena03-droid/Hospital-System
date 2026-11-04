from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment, Patient
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import PatientRegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    doctors = Doctor.objects.all()
    
    return render(request, 'core/home.html', {'doctors': doctors})


# Booking an appointment
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Check if the user is logged in
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to book an appointment.")
        return redirect('login')
    
    # Get the Patient profile of the logged-in user
    # (We use filter().first() to avoid crashing if the user is a Doctor/Admin without a Patient profile)
    patient = Patient.objects.filter(user=request.user).first()
    
    if not patient:
        messages.error(request, "You do not have a Patient profile. Please contact support.")
        return redirect('home')
    
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        
        if date_str and time_slot:
            
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
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome Back, {username}")
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
            
            
@login_required
def doctor_dashboard(request):
    # Check if the logged-in user is actually a Doctor
    doctor = Doctor.objects.filter(user=request.user).first()
    
    
    if not doctor:
        messages.error(request, "You do not have permission to view the doctor dashboard.")
        return redirect('home')
    
    # Get all appointments for this specific doctor, ordered by date
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time_slot')
    
        
    return render(request, 'core/doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
    })
    
    

@login_required
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Security check: ensure the logged-in doctor owns this appointment
    if appointment.doctor.user == request.user:
        appointment.status = 'Completed'
        appointment.save()
        messages.success(request, "Appointment marked as completed.")
    
    return redirect('doctor_dashboard')



@login_required
def patient_dashboard(request):
    # 1. Get the logged-in patient's profile
    patient = Patient.objects.filter(user=request.user).first()
    
    if not patient:
        messages.error(request, "You do not have a Patient profile.")
        return redirect('home')
        
    # 2. Get their appointments (ordered by newest first)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time_slot')
    
    return render(request, 'core/patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments
    })