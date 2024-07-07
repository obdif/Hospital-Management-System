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
from django.http import JsonResponse
from django.db.models import Q




# +++++++++++++================================== SEARCH VIEWS ======================



@login_required(login_url="doctor_login")
def patient_search(request):
    query = request.POST.get('query')
    if query:
        patients = Patient.objects.filter(
            Q(id__icontains=query) | Q(name__icontains=query) | Q(email__icontains=query)
        )
    else:
        patients = Patient.objects.none()

    context = {
        'patients': patients,
    }
    return render(request, "doctors_template/patients_details.html", context)

@login_required(login_url="doctor_login")
def search_autocomplete(request):
    query = request.GET.get('query', '')
    suggestions = []
    if query:
        patients = Patient.objects.filter(
            Q(id__icontains=query) | Q(name__icontains=query) | Q(email__icontains=query)
        ).values('id', 'name', 'email')[:10]
        suggestions = list(patients)
    return JsonResponse(suggestions, safe=False)



# ==================================== DASHBOARD VIEWS =======================

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
    patients = Patient.objects.all().order_by('-id')


    context={
        'patients': patients,
    }
 
    return render(request,"doctors_template/patients.html", context)




@login_required(login_url="doctor_login")
def patients_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    
    context={
        'patient': patient,
    }
 
    return render(request,"doctors_template/patients_details.html", context)



def add_patients(request):
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        age = request.POST.get('age', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        sex = request.POST.get('sex', '')
        address = request.POST.get('address', '')


        context = {
            'name':name,
            'age':age,
            'phone':phone,
            'email':email,
            'sex':sex,
            'address':address,
        }
              
        
        # Check if email already exists
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "doctors_template/add_patient.html", context)


        
        patient = Patient(name=name, age=age, phone_no=phone, email=email, sex=sex, address=address)
        patient.save()
        return redirect('doctor_patients')
 
    return render(request,"doctors_template/add_patient.html")

def invoices(request):
 
    return render(request,"doctors_template/invoices.html")

def doctor_profile(request):
 
    return render(request,"doctors_template/doctor_profile.html")



# ================================== DOCTOR ACCEPT APPOINTMENT UPDATE ==============================
def accept_appointment(appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.accept()
    return HttpResponseRedirect(reverse('doctor_appointments'))


# ================================== DOCTOR REJECT APPOINTMENT UPDATE ==============================

def reject_appointment(appointment_id):
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
                    from_time = from_time.strip()
                    to_time = to_time.strip()
                    if from_time and to_time:  # Ensure both times are still non-empty after stripping
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
        'doctor': doctor,
        'available_days': available_days,
    }

    return render(request, "doctors_template/doctor_available.html", context)



# @login_required(login_url="doctor_login")
# def doctor_available(request):
#     user = request.user
#     doctor = Doctor.objects.get(customuser_ptr=user)

#     if request.method == 'POST':
#         days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#         for day in days:
#             if request.POST.get(f'{day}_available'):
#                 from_time = request.POST.get(f'{day}_from').strip()
#                 to_time = request.POST.get(f'{day}_to').strip()
#                 if from_time and to_time:
#                     print(f"Saving: {day} from {from_time} to {to_time}")
#                     DoctorAvailableDay.objects.update_or_create(
#                         doctor=doctor,
#                         day=day,
#                         defaults={'from_time': from_time, 'to_time': to_time}
#                     )

#         return redirect('doctor_appointments')

#     availabilities = DoctorAvailableDay.objects.filter(doctor=doctor)
#     available_days = {availability.day: availability for availability in availabilities}
#     days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

#     context = {
#         'availabilities': availabilities,
#         'days_of_week': days_of_week,
#         'doctor': doctor,
#         'available_days': available_days,
#     }

#     return render(request, "doctors_template/doctor_available.html", context)

def appointment_details(request, appointment_id):
    doctor = Doctor.objects.get(customuser_ptr=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == "POST":
        condition = request.POST.get('cp', '')
        note = request.POST.get('note', '')
        
        
        appointment.condition = condition
        appointment.doctor_note = note
        if 'accept' in request.POST:
            appointment.accept()
        elif 'reject' in request.POST:
            appointment.reject()
        appointment.save()

        messages.success(request, "Feedback Sent successfully")
        return redirect('appointment_details', appointment_id=appointment_id)
    
    context= {
        "patient":appointment.patient,
        "appointment":appointment,
        "doctor":doctor,
        # "pending_appointment":pending_appointment,
        # "rejected_appointments":rejected_appointments,
    }
    return render(request, "doctors_template/appointment_details.html", context)


def doctors(request):
 
    return render(request,"doctors_template/doctors.html")



def department(request):
 
    return render(request,"doctors_template/department.html")




def logout_doctor(request):
    logout(request) 
    return redirect('doctor_login')



