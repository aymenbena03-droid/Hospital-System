from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment, Patient
from django.contrib import messages
from django.db import IntegrityError

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