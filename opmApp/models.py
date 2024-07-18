from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import random
from django.utils import timezone

# SUPER_USER DETAILS:
# username: blessing 
# email: blessing@gmail.com
# password: blessing


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique=True) 
    name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200, unique=True)
    profile_pic = models.ImageField(upload_to="profile/", blank=True, default="https://res.cloudinary.com/dbqtos6rt/image/upload/v1720589104/opms/profile/profile_bgrbul.jpg")
    phone_no = models.IntegerField( blank=False, default=2)
    address = models.TextField(max_length=500, blank=True, default="")
    sex = models.CharField(max_length= 10, default="")
    country = models.CharField(max_length=20, blank=True, default="Nigeria")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'name']
    
    
    def __str__(self):
        return self.name or self.email



class Patient(CustomUser):
    age = models.IntegerField()
    patient_id = models.CharField(max_length=12, unique=True, editable=False)
    blood_group = models.CharField(max_length=5, blank=True, default="")
    password=None
    
    
    # USERNAME_FIELD = 'email' 
    

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = self.generate_patient_id()
        super().save(*args, **kwargs)

    def generate_patient_id(self):
        id_prefix = "LUTH"
        year = datetime.now().strftime("%y")
        while True:
            new_id = random.randint(0, 9999)  # Generate a random 4-digit number
            patient_id = f"{id_prefix}{year}{new_id:04d}"
            if not Patient.objects.filter(patient_id=patient_id).exists():
                break
        return patient_id
    
    def __str__(self):
        return self.name
    
 
 
class Department(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(blank=True, default="", upload_to="assets/")
    
    def __str__(self):
        return self.name    



class Doctor(CustomUser):
    status=models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    document = models.ImageField(upload_to='doctor_documents/', null=True, blank=True)
    about = models.TextField(blank=True, default="---")
    
    
    def __str__(self):
        return self.name




class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    condition = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    date_time = models.CharField(max_length=10)
    doctor_note = models.TextField(blank=True)
    time = models.CharField(max_length=10)
    current_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor_id.name} for {self.patient.name} on {self.date_time}"
    
    def accept(self):
        self.status = 'Accepted'
        self.save()
    
    def reject(self):
        self.status = 'Rejected'
        self.save()


class DoctorAvailableDay(models.Model):
    DOCTOR_DAYS = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DOCTOR_DAYS)
    from_time = models.TimeField()
    to_time = models.TimeField()
    
    class Meta:
        unique_together = ('doctor', 'day') 

    def __str__(self):
        return f"{self.doctor.username} - {self.day} from {self.from_time} to {self.to_time}"
    
    


class MedicalResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default='')
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    recordNumber = models.CharField(max_length=12, unique=True, editable=False)
    assignedDoctorName=models.CharField(Doctor, max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    condition_before = models.CharField(max_length=100, null=True)
    condition_after = models.CharField(max_length=100, null=True)
    
    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
    
    
    dischargeMeditations = models.CharField(max_length=200)
    dischargeInstructions = models.TextField(max_length=500)
    
    
    
    def save(self, *args, **kwargs):
        if not self.recordNumber:
            self.recordNumber = self.invoiceNumber()
        super().save(*args, **kwargs)

    def invoiceNumber(self):
        year = datetime.now().strftime("%y")
        while True:
            new_id = random.randint(0, 999999)  # Generate a random 6-digit number
            recordNumber = f"{year}{new_id:06d}"
            if not MedicalResult.objects.filter(recordNumber=recordNumber).exists():
                break
        return recordNumber
    
    
    def __str__(self):
        return self.patient
