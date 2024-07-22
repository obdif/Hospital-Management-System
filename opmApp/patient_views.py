from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.core.files.storage import default_storage





@login_required(login_url="patient_login")
def patient_dashboard(request):
    # doctors = Doctor.objects.all()
    patient = Patient.objects.get(id=request.user.id)
    appointments = Appointment.objects.filter(patient=request.user).order_by('-current_date')
    pending_appointments = appointments.filter(status='Pending').count()
    rejected_appointments = appointments.filter(status='Rejected').count()
    

  
    context ={
        # 'patient_id': patient.patient_id,
        # 'phone_no' : patient.phone_no,
        # 'name': patient.name,
        # 'age': patient.age,
        # 'email': patient.email,
        # 'address': patient.address,
        # 'profile': patient.profile_pic,
        'patient':patient,
        'appointments': appointments,
        'pending_appointments':pending_appointments,
        'rejected_appointments':rejected_appointments,
    }
    return render(request,"patients_template/patient_dashboard.html", context)



def patient_register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        age = request.POST.get('age', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        sex = request.POST.get('sex', '')


        context = {
            'name':name,
            'age':age,
            'phone':phone,
            'email':email,
            'sex':sex,
        }
              
        
        # Check if email already exists
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "patients_template/patient_register.html", context)


        
        patient = Patient(name=name, age=age, phone_no=phone, email=email, sex=sex)
        patient.save()

        # if patient is not None:
        #     messages.error(request, "Registration failed. Please try again.")

        subject = "LUTH | PATIENT REGISTRATION SUCCESSFUL"
        message = f"Welcome {name}! \n\n\nThanks for your registration. Your Paitient ID to log in to the portal is: \n\n{patient.patient_id}\n\n\n\n Kindly visit www.luth.com/login to log in"
        sender = 'adeblessinme4u@gmail.com'
        receiver = [email]
        send_mail(subject, message, sender, receiver, fail_silently=True)

        return redirect('patient_registration_confirmation')

 
    return render(request,"patients_template/patient_register.html")


#  ====================================================== REGISTRATION CONFIRMATION VIEW ==========================================
def patient_registration_confirmation(request):

    messages.success(request, "Registration successful!")
    if request.method == 'POST':
        # pass#don't forget to remove this "pass" ====================
        return redirect("patient_login")
    else:
        pass
    

    return render(request, "patients_template/patient_registration_confirmation.html")



def patient_login(request):
    if request.method == "POST":
        patient_id = request.POST.get('yourId').upper()
        
        patient = authenticate(request, username=patient_id)
        
        if patient is not None:
            login(request, patient)
            # messages.success(request, "Login successful!")
            return redirect("patient_dashboard")
        
        else:
            messages.error(request, "Invalid Patient ID. please try again.")
            return render(request, "patients_template/patient_login.html", {'patient_id':patient_id})
     
    return render(request,"patients_template/patient_login.html")


@login_required(login_url="patient_login")
def book_an_appointment(request):
    doctors = Doctor.objects.all()
    patient = Patient.objects.get(id=request.user.id)

    if request.method == "POST":
        description = request.POST.get('description', '')
        doctor_id = request.POST.get('doctor', '')
        date_str = request.POST.get('date')
        time = request.POST.get('time')
        
        
        context ={
            "description": description,
            "doctors": doctors,
            "doctor_id": doctor_id,
        }
        
        # ============ code to check the length of discription, it must be greater than 10 character ====
        
        # if len(description) < 10:
        #     messages.error(request, "Explanation is too short.")
        #     return render(request, "patients_template/book_an_appointment.html", context)
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExitst:
            messages.error(request, "Selected doctor does not exist")
            return render(request, "patients_template/book_an_appointment.html", context)

        
        # try:
        #     date = datetime.strptime(date_str, "%Y-%m-%d").date()
        # except ValueError:
        #     messages.error(request, "Invalid date format. Please use YYYY-MM-DD format.")
        #     return render(request, "patients_template/book_an_appointment.html", context)
        
        patient = patient  # Use the patient object obtained earlier

        appointment = Appointment(patient=patient, doctor_id=doctor, description=description, date_time=date_str, time=time)
        appointment.save()

        messages.success(request, "Appointment sent!")
        return redirect("patient_appointments")
        
        # patient = request.user    
        
        # appointment = Appointment(patient=patient, doctor_id=doctor, description=description, date_time=date, time=time)
        # appointment.save()
        
        # messages.success(request, "Appointment sent!")
        # return redirect("patient_appointments")
      
    context={
        "doctors":doctors,
        "patient": patient,
    }
 
    return render(request,"patients_template/book_an_appointment.html", context)


@login_required(login_url="patient_login")
def fetch_available_times(request):
    doctor_id = request.GET.get('doctor_id')
    availabilities = DoctorAvailableDay.objects.filter(doctor_id=doctor_id)
    
    dates = []
    times = []
    
    for availability in availabilities:
        dates.append(f"<option value='{availability.day}'>{availability.day}</option>")
        times.append(f"<option value='{availability.from_time}'>{availability.from_time} - {availability.to_time}</option>")
    
    return JsonResponse({
        'dates': ''.join(dates),
        'times': ''.join(times),
    })



@login_required(login_url="patient_login")
def patient_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-current_date')
    patient = Patient.objects.get(id=request.user.id)
    
    
    context = {
        'appointments': appointments,
        'patient': patient,
        # 'pending_appointments_count': pending_appointments_count,
        # 'rejected_appointments_count': rejected_appointments_count,
    }
    return render(request, "patients_template/patient_appointments.html", context)


# =================== EDIT APPOINTMENT -====================

@login_required(login_url="patient_login")
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    doctors = Doctor.objects.all()
    patient = Patient.objects.get(id=request.user.id)

    if request.method == 'POST':
        description = request.POST.get('description')
        doctor_id = request.POST.get('doctor')    
        date = request.POST.get('date')
        time = request.POST.get('time')
        
                # Combine date and time into a single datetime object
        # date_time_str = f"{date} {time}"
        # try:
        #     date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        # except ValueError:
        #     # Handle the case where the date or time format is incorrect
        #     return render(request, 'edit_appointment.html', {'error': 'Invalid date or time format', 'appointment': appointment})

        status_ = appointment.status == 'Pending'
        datenow = timezone.now()
      
        if description:
            appointment.description = description
        if doctor_id:
            appointment.doctor_id_id = doctor_id
        if date:
            appointment.date_time = date
        if time:
            appointment.time = time
        if datenow:
            appointment.current_date = datenow
        
        appointment.status= "Pending"
        
        appointment.save()
        messages.success(request, "Appointment updated successfully")
        return redirect('patient_appointments')
    
    return render(request, 'patients_template/edit_appointment.html', {'appointment':appointment, 'doctors':doctors, 'patient':patient})

# =========================== DELETE APPOINTMENTS =======================
@login_required(login_url="patient_login")
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
        return redirect('patient_appointments')
    


@login_required(login_url="patient_login")
def appointment_details(request, appointment_id):
    patient = Patient.objects.get(id=request.user.id)
    appointment = get_object_or_404(Appointment, id=appointment_id)

    context = {
        'patient': patient,
        'appointment': appointment,

    }
    return render(request, "patients_template/appointment_details.html", context)


@login_required(login_url="patient_login")
def medical_historys(request):
    
    return render(request, "patients_template/medical_historys.html")

def medical_result_receipt(request):
    
    return render(request, "patients_template/medical_result_receipt.html")


@login_required(login_url="patient_login")
def doctors(request):
    patient = Patient.objects.get(id=request.user.id)
    doctors = Doctor.objects.all()


    context={
        'patient':patient,
        'doctors':doctors,
    }
 
    return render(request,"patients_template/doctors.html", context)


@login_required(login_url="patient_login")
def department(request):
 
    return render(request,"patients_template/departments.html")


@login_required(login_url="patient_login")
def patient_profile(request):
    patient = Patient.objects.get(id=request.user.id)
    if request.method == 'POST':
        patient.name = request.POST.get('name', '')
        patient.age = request.POST.get('age', '')
        patient.phone_no = request.POST.get('phone', '')
        patient.address = request.POST.get('address', '')
        patient.country = request.POST.get('country', '')
        patient.sex = request.POST.get('gender', '')



      
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            patient.profile_pic = default_storage.save(f"profile/{profile_image.name}", profile_image)

        messages.success(request, "Account updated successfully.")
        patient.save()
        return redirect('patient_profile')
    
    
    context = {
        'patient': patient,
    }
 
    return render(request,"patients_template/patient_profile.html", context)



def logout_patient(request):
    logout(request) 
    return redirect('patient_login')


