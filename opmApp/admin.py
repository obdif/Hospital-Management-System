from django.contrib import admin
from . import models



class PatientAdmin(admin.ModelAdmin):
    list_display=('name', 'patient_id', 'email', 'phone_no', 'profile_pic')

class CustomAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    
class DoctorAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'department', 'status')
    
class AppointmentAdmin(admin.ModelAdmin):
    list_display=('doctor_id', 'patient', 'description', 'date_time', 'status')
    
class DoctorAvailableDayAdmin(admin.ModelAdmin):
    list_display=('doctor', 'day', 'from_time', 'to_time')
    

    
# ====================== REGISTRATION OF MODELS =================

admin.site.register(models.CustomUser, CustomAdmin)
admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Department)
admin.site.register(models.Appointment, AppointmentAdmin)
admin.site.register(models.MedicalResult)
admin.site.register(models.DoctorAvailableDay, DoctorAvailableDayAdmin)
admin.site.register(models.OTP)