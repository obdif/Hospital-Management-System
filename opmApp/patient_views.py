from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django.core.files.storage import default_storage
from datetime import datetime





@login_required(login_url="patient_login")
def patient_dashboard(request):
    # doctors = Doctor.objects.all()
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')

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

        subject = "LUTH | PATIENT REGISTRATION SUCCESSFUL"
        message = f"Welcome {name}! \n\n\nThanks for your registration. Your Paitient ID to log in to the portal is: \n\n{patient.patient_id}\n\n\n\n Kindly visit (https://hospital-management-system-kohl.vercel.app/patient/) to log in"
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
        
        # try:
        #     patient = Patient.objects.get(id=request.user.id)
        # except Doctor.DoesNotExist:
        #     return redirect('patient_login')
        
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
        
        context={}
        
        description = request.POST.get('description', '')
        doctor_id = request.POST.get('doctor', '')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
       
        # # Validate the combined string
        # try:
        #     date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        # except ValueError:
        #     messages.error(request, "Invalid date or time format. Please try again.")
        #     return render(request, "patients_template/book_an_appointment.html", context)

        doctor = Doctor.objects.get(id=doctor_id)
        patient = Patient.objects.get(id=request.user.id)

        appointment = Appointment(
            patient=patient, 
            doctor_id=doctor, 
            description=description, 
            date_time=date_str, 
            time=time_str
        )
        appointment.save()



        subject = f"{patient.name} BOOKED AN APPOINTMENT WITH YOU ON {date_str} at {time_str}"
        message = (
            f"Hello Dr. {doctor.name}!\n\nYou have an appointment with {patient.name} "
            f"on {date_str} at {time_str}.\n\nComplaint: {description}\n\n"
            "Kindly log in to your account to accept or reject the appointment.\n\n"
            "Log in here: (https://hospital-management-system-kohl.vercel.app/doctor/)"
        )
        sender = 'adeblessinme4u@gmail.com'
        receiver = [doctor.email]
        send_mail(subject, message, sender, receiver, fail_silently=True)

        messages.success(request, "Appointment booked successfully!")
        return redirect("patient_appointments")

    context = {
        "doctors": doctors,
        "patient": patient,
    }

    return render(request, "patients_template/book_an_appointment.html", context)





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
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')

    
    
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
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')

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
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    context = {
        'patient': patient,
        'appointment': appointment,

    }
    return render(request, "patients_template/appointment_details.html", context)


@login_required(login_url="patient_login")
def medical_historys(request):
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')

    invoices= MedicalResult.objects.filter(patient=request.user).order_by('-id')
    

    
    
    context ={
        'patient':patient,
        'invoices':invoices,
        # 'paidInvoice':paidInvoice,
        # 'Pending':Pending,
    }
    return render(request, "patients_template/medical_historys.html", context)


def medical_result_receipt(request, invoice_id):
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')
    
    invoice = get_object_or_404(MedicalResult, id=invoice_id)
    
    context ={
        'patient':patient,
        'invoice':invoice,
    }
    
    return render(request, "patients_template/medical_result_receipt.html", context)



@login_required(login_url="patient_login")
def patient_doctors(request):
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')

    doctors = Doctor.objects.all()


    context={
        'patient':patient,
        'doctors':doctors,
    }
 
    return render(request,"patients_template/doctors.html", context)


@login_required(login_url="patient_login")
def patient_departments(request):
 
    return render(request,"patients_template/departments.html")


@login_required(login_url="patient_login")
def patient_profile(request):
    try:
        patient = Patient.objects.get(id=request.user.id)
    except Patient.DoesNotExist:
        return redirect('patient_login')

    if request.method == 'POST':
        patient.name = request.POST.get('name', '')
        patient.age = request.POST.get('age', '')
        patient.phone_no = request.POST.get('phone', '')
        patient.address = request.POST.get('address', '')
        patient.country = request.POST.get('country', '')
        # patient.sex = request.POST.get('gender', '')



      
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


def recover_id(request):
    if request.method == "POST":
        email = request.POST.get('email', '')

        if Patient.objects.filter(email=email).exists():
            patient = Patient.objects.get(email=email)

            subject = "PATIENT ID RECOVERY"
            message = f"Your Patient ID is \n {patient.patient_id}"
            sender = 'adeblessinme4u@gmail.com'
            receiver = [email]
            send_mail(subject, message, sender, receiver, fail_silently=True)

            messages.success(request, f"Your patient ID is: {patient.patient_id}.")
            return redirect("patient_login")
        else:
            messages.error(request, f"{email} is not a registered Patient. Please check the email and try again.")
            return render(request, 'patients_template/recover_id.html')

        
        
    return render(request, 'patients_template/recover_id.html')


def logout_patient(request):
    logout(request) 
    return redirect('patient_login')


