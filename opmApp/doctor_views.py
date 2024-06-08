from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail







@login_required(login_url="doctor_login")
def doctor_dashboard(request):
    doctor = Doctor.objects.get(id=request.user.id)
    total_patient = Patient.objects.count()
    doctor_appointments = Appointment.objects.filter(doctor_id=request.user)
    upcoming_appoinments = doctor_appointments.filter(status='Pending').order_by('-date_time')[:2]
    approved_appointments = doctor_appointments.filter(status='Accepted').order_by('-date_time')[:2]
    
    
    context = {
        'total_patient': total_patient,
        'doctor_appointments': doctor_appointments,
        'doctor': doctor,
        'upcoming_appoinments': upcoming_appoinments,
        'approved_appointments': approved_appointments,
    }
 
    return render(request,"doctors_template/doctor_dashboard.html", context)



def doctor_register(request):
    departments = Department.objects.all()
    if request.method == "POST":
        name = request.POST.get('name', '')
        department = request.POST.get('department')
        file = request.FILES.get('file', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        C_password = request.POST.get('Cpassword', '')
        
        
        context ={
            'name': name,
            'email': email,
            'password': password,
            'C_password': C_password,
            'department': department,
            'departments':departments,
            'file': file,
            
        }
        
            # Check if email already exists
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'doctors_template/doctor_register.html', context)
        else:
            pass
        
        
          # =================== TO VALIDATE THE FILE DOCTOR UPLOAD ======== 
        if file:
            if file.content_type not in ['image/png', 'image/jpeg', 'application/pdf']:
                messages.error(request, 'File type not supported. Please upload a .png, .jpeg, or .pdf file.')
                return render(request, 'doctors_template/doctor_register.html', context)
            if file.size > 5 * 1024 * 1024:
                messages.error(request, 'File size should not exceed 5 MB.')
                return render(request, 'doctors_template/doctor_register.html', context)
        
        
        # ============================ TO VALIDATE PASSWORD ==============
        
        if password != C_password:
            messages.error(request, "Password do not match!")
        elif len(password) < 8:
            messages.error(request, "Password must be greater than 8 Character.")
            return render(request, 'doctors_template/doctor_register.html', context)

        
        
                # ============================ TO VALIDATE DEPARTMENT ==============

        if not department:
            messages.error(request, "Please select a department.")
            return render(request, 'doctors_template/doctor_register.html', context)
        
        try:
            department = Department.objects.get(id=department)
        except Department.DoesNotExist:
            messages.error(request, "Invalid department selected")
            return render(request, 'doctors_template/doctor_register.html', context)
        
        
        
        username = email.split('@')[0]  # Simple username generation based on email
        
        # Create doctor user
        doctor = Doctor.objects.create_user(username=username, name=name, email=email, department=department, password=C_password)
        doctor.set_password(C_password)
        doctor.save()
        
        if file:
            doctor.file = file
            doctor.save()
            
                 # Set the backend attribute on the user
        backend = get_backends()[0]
        doctor.backend = f'{backend.__module__}.{backend.__class__.__name__}'

        login(request, doctor)
        
        messages.success(request, "Registration successful!")
        return redirect('doctor_login')


 
    return render(request,"doctors_template/doctor_register.html", {'departments': departments})




def doctor_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
 
        authenticate_user = authenticate(email=email, password=password)
        if authenticate_user is not None:
            login(request, authenticate_user)
            return redirect('doctor_dashboard')
        
        else:
            messages.error(request, "Wrong Credentials details.\n Try again.")
            return redirect('doctor_login')
 
    return render(request,"doctors_template/doctor_login.html")


@login_required(login_url="doctor_login")
def patients(request):
 
    return render(request,"doctors_template/patients.html")


def add_patients(request):
 
    return render(request,"doctors_template/add_patient.html")

def invoices(request):
 
    return render(request,"doctors_template/invoices.html")

def doctor_profile(request):
 
    return render(request,"doctors_template/doctor_profile.html")



# ================================== DOCTOR ACCEPT APPOINTMENT UPDATE ==============================
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.accept()
    return HttpResponseRedirect(reverse('doctor_appointments'))


# ================================== DOCTOR REJECT APPOINTMENT UPDATE ==============================

def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.reject()
    return HttpResponseRedirect(reverse('doctor_appointments'))




# ================================== DOCTOR APPOINTMENT  ==============================

def doctor_appointments(request):
    doctor = Doctor.objects.get(id=request.user.id)
    appointments = Appointment.objects.filter(doctor_id=request.user).order_by('-current_date')

    
    
    
    
    context = {
        'doctor':doctor,
        'appointments':appointments,
    }
 
    return render(request,"doctors_template/doctor_appointments.html", context)


# ================================== APPOINTMENT  VIEW DETAILS ==============================
@login_required(login_url="doctor_login")
def doctor_available(request):
    user = request.user
    doctor = Doctor.objects.get(customuser_ptr=user)

    if request.method == 'POST':
      
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for day in days:
            if request.POST.get(f'{day}_available'):
                from_time = request.POST.get(f'{day}_from')
                to_time = request.POST.get(f'{day}_to')
                if from_time and to_time:
                    DoctorAvailableDay.objects.create(
                        doctor=doctor,
                        day=day,
                        from_time=from_time,
                        to_time=to_time
                    )
                    
      
        return redirect('doctor_appointments')

    availabilities = DoctorAvailableDay.objects.filter(doctor=doctor)
    available_days = {availability.day: availability for availability in availabilities}
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


    context = {
            'availabilities': availabilities,
            'days_of_week': days_of_week,
            'available_days': available_days,
        }
    
    
    return render(request, "doctors_template/doctor_available.html", context)


def appointment_details(request):
    
    return render(request, "doctors_template/appointment_details.html")


def doctors(request):
 
    return render(request,"doctors_template/doctors.html")



def department(request):
 
    return render(request,"doctors_template/department.html")




def logout_doctor(request):
    logout(request) 
    return redirect('doctor_login')



