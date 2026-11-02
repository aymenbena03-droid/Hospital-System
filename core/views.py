from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment, Patient
from django.contrib import messages
from datetime import datetime

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
            
            # Create an appointment
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=date_str,
                time_slot=time_slot,
                status='Pending'
            )
            messages.success(request, 'Appointement booked successfully!')
            return redirect('home')
    
    return render(request, 'core/book_appointment.html', {'doctor': doctor})