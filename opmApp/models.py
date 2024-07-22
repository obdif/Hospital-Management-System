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
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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
    patientName = models.CharField(max_length=100, default="")
    assignedDoctorName = models.CharField(max_length=100, default="")
    # address = models.CharField(max_length=255, default="")
    condition_before = models.TextField(default="")
    condition_after = models.TextField(default="Good Health")
    admitDate = models.DateField()
    releaseDate = models.DateField()
    daySpent = models.IntegerField()
    roomCharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medicineCost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    doctorFee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    OtherCharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    history_of_illness = models.TextField(blank=True, default="Not Applicable")
    dischargeMeditations = models.TextField(default="Not Applicable")
    dischargeInstructions = models.TextField(blank=False)
    invoice_id = models.CharField(max_length=20, unique=True, editable=False, default="")
    created_date=models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = self.generate_invoice_id()
        self.total = self.roomCharge + self.medicineCost + self.doctorFee + self.OtherCharge
        super().save(*args, **kwargs)

    def generate_invoice_id(self):
        prefix = "INV"
        year = datetime.now().strftime("%y")
        while True:
            new_id = random.randint(0, 99999)
            invoice_id = f"{prefix}{year}{new_id:05d}"
            if not MedicalResult.objects.filter(invoice_id=invoice_id).exists():
                break
        return invoice_id
    
    def __str__(self):
        return f'{self.patientName} - {self.invoice_id}'
