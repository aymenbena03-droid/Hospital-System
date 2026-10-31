from django.db import models
from django.contrib.auth.models import User

# 1. Department Model (科室)
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 2. Doctor Profile Model (医生)
class Doctor(models.Model):
    # Link to the built-in User model (for login)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    # The avatar/photo for the doctor
    avatar = models.ImageField(upload_to='doctors/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Dr. {self.user.last_name} - {self.department.name}"

# 3. Patient Profile Model (患者)
class Patient(models.Model):
    # Link to the built-in User model (for login)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

# 4. Appointment Model (预约记录)
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', '待就诊'),
        ('Completed', '已完成'),
        ('Cancelled', '已取消'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=50) # e.g., "09:00 - 09:30"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This prevents the same doctor from being booked twice at the exact same time
        unique_together = ('doctor', 'date', 'time_slot')

    def __str__(self):
        return f"{self.patient.user.username} with {self.doctor.user.last_name} on {self.date} at {self.time_slot}"