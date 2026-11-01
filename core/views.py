from django.shortcuts import render
from .models import Doctor

# Create your views here.

def home(request):
    doctors = Doctor.objects.all()
    
    return render(request, 'home.html', {'doctors': doctors})