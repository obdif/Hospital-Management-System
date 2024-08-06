from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import get_user_model
from .forms import PatientSearchForm
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
import logging
from django.http import JsonResponse
from django.db.models import Q
from django.core.files.storage import default_storage
from decimal import Decimal, InvalidOperation






# ==================================== DASHBOARD VIEWS =======================

@login_required(login_url="doctor_login")
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        return redirect('doctor_login')
    
    if doctor.status== "Pending":
        messages.error(request, "Your Account is still under review.")
        return redirect('doctor_login')
    else:
        pass
    
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
        
        

        
                # ============================ TO VALIDATE DEPARTMENT ==============

        if not department:
            messages.error(request, "Please select a department.")
            return render(request, 'doctors_template/doctor_register.html', context)
        
        try:
            department = Department.objects.get(id=department)
        except Department.DoesNotExist:
            messages.error(request, "Invalid department selected")
            return render(request, 'doctors_template/doctor_register.html', context)
        
                # ============================ TO VALIDATE PASSWORD ==============
        
        if password != C_password:
            messages.error(request, "Password do not match!")
        elif len(password) < 8:
            messages.error(request, "Password must be greater than 8 Character.")
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
 
        # context = {
        #     'email':email,
        # }
        
        authenticate_user = authenticate(email=email, password=password)
        
        
        if authenticate_user is not None:
            login(request, authenticate_user)
            return redirect('doctor_dashboard')
        
        else:
            messages.error(request, "Wrong Credentials details.\n Try again.")
            return redirect('doctor_login')
        
        # messages.error(request, "Your Account is still under review.")
 
    return render(request,"doctors_template/doctor_login.html")




@login_required(login_url="doctor_login")
def patients(request):
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        return redirect('doctor_login')
    # doctor = Doctor.objects.get(id=request.user.id)
    patients = Patient.objects.all().order_by('-id')


    context={
        'patients': patients,
        'doctor': doctor,
    }
 
    return render(request,"doctors_template/patients.html", context)




@login_required(login_url="doctor_login")
def patients_details(request, patient_id):
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        return redirect('doctor_login')
    patient = get_object_or_404(Patient, id=patient_id)
    # patient = Patient.objects.get(id=request.user.id)
    if request.method == 'POST':
        patient.name = request.POST.get('name', '')
        patient.age = request.POST.get('age', '')
        patient.phone_no = request.POST.get('phone', '')
        patient.address = request.POST.get('address', '')
        patient.country = request.POST.get('country', '')
        patient.sex = request.POST.get('gender', '')
        patient.blood_group = request.POST.get('bgroup', '')



      
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            patient.profile_pic = default_storage.save(f"profile/{profile_image.name}", profile_image)

        messages.success(request, "Patient updated successfully.")
        patient.save()
        return redirect('patients_details', patient_id=patient_id)
    
    
    
    context={
        'patient': patient,
        'doctor': doctor,
    }
 
    return render(request,"doctors_template/patients_details.html", context)


# +++++++++++++================================== SEARCH VIEWS ======================




@login_required(login_url="doctor_login")
def search_patients(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        results = Patient.objects.filter(
            Q(patient_id__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query)
        ).values('id', 'patient_id', 'name', 'email')
        return JsonResponse(list(results), safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url="doctor_login")
def search_autocomplete(request):
    query = request.GET.get('query', '')
    suggestions = []
    if query:
        patients = Patient.objects.filter(
            Q(patient_id__icontains=query) | Q(name__icontains=query) | Q(email__icontains=query)
        ).values('patient_id', 'name', 'email')[:10]
        suggestions = list(patients)
    return JsonResponse(suggestions, safe=False)



@login_required(login_url="doctor_login")
def add_patients(request):
    # doctor = Doctor.objects.get(id=request.user.id)
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




@login_required(login_url="doctor_login")
def patient_search(request):
    query = request.GET.get('query', '')
    patients = Patient.objects.filter(
        Q(patient_id__icontains=query) | 
        Q(email__icontains=query) | 
        Q(name__icontains=query)
    )
    suggestions = list(patients.values('id', 'patient_id', 'name', 'email'))
    return JsonResponse(suggestions, safe=False)

@login_required(login_url="doctor_login")
def create_invoice(request):
    if request.method == 'GET' and 'patient_info' in request.GET:
        patient_info = request.GET['patient_info']
        try:
            patient = Patient.objects.get(
                Q(patient_id=patient_info) | Q(email=patient_info) | (Q(phone_no=patient_info) if patient_info.isdigit() else Q())
            )
            return redirect('create_invoice_with_patient', patient_id=patient.id)
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found.")
            return redirect('invoices')  # Redirect to the invoices tracking page

    return render(request, 'doctors_template/create_invoice.html')





@login_required(login_url="doctor_login")
def create_invoice_with_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        return redirect('doctor_login')

    if request.method == 'POST':
        try:
            room_charge = Decimal(request.POST.get('roomCharge', '0'))
            medicine_cost = Decimal(request.POST.get('medicineCost', '0'))
            doctor_fee = Decimal(request.POST.get('doctorFee', '0'))
            other_charge = Decimal(request.POST.get('OtherCharge', '0'))
        except InvalidOperation:
            messages.error(request, "Please enter valid numbers for charges.")
            return redirect('create_invoice_with_patient', patient_id=patient_id)

        MedicalResult.objects.create(
            patient=patient,
            doctor=doctor,  # Explicitly assign the doctor
            patientName=patient.name,
            assignedDoctorName=request.user.username,
            condition_before=request.POST.get('condition_before', ''),
            condition_after=request.POST.get('condition_after', ''),
            admitDate=request.POST.get('admitDate', ''),
            releaseDate=request.POST.get('releaseDate', ''),
            roomCharge=room_charge,
            medicineCost=medicine_cost,
            doctorFee=doctor_fee,
            OtherCharge=other_charge,
            dischargeMeditations=request.POST.get('dischargeMeditations', ''),
            dischargeInstructions=request.POST.get('dischargeInstructions', ''),
        )
        
        
        context = {
            'condition_before':MedicalResult.condition_before,
            'condition_after':MedicalResult.condition_after,
            'dischargeMeditations':MedicalResult.dischargeMeditations,
            'dischargeInstructions':MedicalResult.dischargeInstructions,
            # 'sex':sex,
            # 'address':address,
        }
        
        
        
        messages.success(request, "Invoice created successfully.")
        return redirect('invoices')  # Redirect to the invoices tracking page

    context = {
        'patient': patient,
        'doctor': doctor,
    }
    return render(request, 'doctors_template/create_invoice.html', context)



@login_required(login_url="doctor_login")
def invoices(request):
    # invoices = MedicalResult.objects.filter(doctor_id=request.user).order_by('-created_date')
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('doctor_login')  

    invoices = MedicalResult.objects.filter(doctor_id=request.user).order_by('-created_date')
    # invoicePaid=MedicalResult.objects.filter(status='Paid')
    # invoicePending=MedicalResult.objects.filter(status='Pending')

    context = {
        'doctor': doctor,
        'invoices': invoices,
        # 'invoicePaid': invoicePaid,
        # 'invoicePending': invoicePending,
    }
    return render(request, "doctors_template/invoices.html", context)


@login_required(login_url="doctor_login")
def invoice_receipt(request, invoice_id):
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('doctor_login')
    
    invoice = get_object_or_404(MedicalResult, id=invoice_id) 
       
    context ={
        'doctor':doctor,
        'invoice':invoice,
    }
    return render(request, "doctors_template/invoice_receipt.html", context)


def edit_invoice(request, invoice_id):
    # patient = get_object_or_404(Patient, id=patient_id)
    doctor= Doctor.objects.get(id=request.user.id)
    invoice = get_object_or_404(MedicalResult, id=invoice_id)
    
    if request.method == "POST":
        condition_before= request.POST.get('condition_before')
        condition_after= request.POST.get('condition_after')
        admitDate= request.POST.get('admitDate')
        releaseDate= request.POST.get('releaseDate')
        dischargeMeditations=request.POST.get('dischargeMeditations')
    
    
        if condition_before:
            invoice.condition_before = condition_before
        if condition_after:
            invoice.condition_after = condition_after
        if admitDate:
            invoice.admitDate = admitDate
        if releaseDate:
            invoice.releaseDate = releaseDate
        if dischargeMeditations:
            invoice.dischargeMeditations = dischargeMeditations
            
        
        invoice.save()
        messages.error(request, "Edit save")
        return redirect('edit_invoice')
    
    
    context = {
        'doctor':doctor,
        'invoice':invoice,
        # 'patient':patient,
    }
    return render(request, "doctors_template/edit_invoice.html", context)
    





@login_required(login_url="doctor_login")
def doctor_profile(request):
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        return redirect('doctor_login')
    
    if request.method == 'POST':
        doctor.name = request.POST.get('name', '')
        # doctor.age = request.POST.get('age', '')
        doctor.phone_no = request.POST.get('phone', '')
        doctor.about = request.POST.get('about', '')
        doctor.address = request.POST.get('address', '')
        doctor.country = request.POST.get('country', '')



        department_name = request.POST.get('department', '')
        if department_name:
            try:
                department = Department.objects.get(name=department_name)
                doctor.department = department
            except Department.DoesNotExist:
                # Handle the case where the department doesn't exist
                pass
            
      
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            doctor.profile_pic = default_storage.save(f"profile/{profile_image.name}", profile_image)

        messages.success(request, "Account updated successfully.")
        doctor.save()
        return redirect('doctor_profile')
    departments = Department.objects.all()
    
    
    context = {
        'doctor': doctor,
        'departments': departments,
    }
 
    return render(request,"doctors_template/profile.html", context)



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
@login_required(login_url="doctor_login")
def doctor_appointments(request):
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        return redirect('doctor_login')
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
                from_time = request.POST.get(f'{day}_from', '').strip()
                to_time = request.POST.get(f'{day}_to', '').strip()
                if from_time and to_time:
                    DoctorAvailableDay.objects.update_or_create(
                        doctor=doctor,
                        day=day,
                        defaults={'from_time': from_time, 'to_time': to_time}
                    )
                else:
                    messages.error(request, f'Times for {day} are not valid.')

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




@login_required(login_url="doctor_login")
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

@login_required(login_url="doctor_login")
def doctors(request):
    doctors = Doctor.objects.all()
    try:
        doctor = Doctor.objects.get(id=request.user.id)
    except Doctor.DoesNotExist:
        return redirect('doctor_login')
 
 
    context = {
        'doctors':doctors,
        'doctor':doctor,
        }
    return render(request,"doctors_template/doctors.html", context)


@login_required(login_url="doctor_login")
def department(request):
 
    return render(request,"doctors_template/departments.html")


logger = logging.getLogger(__name__)
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        context = {
            'email': email,
        }

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            otp = OTP(email=email)
            otp.save()

            subject = "PASSWORD RESET OTP"
            message = f"Your OTP for password reset is \n\n\n\n{otp.otp}."
            sender = 'adeblessinme4u@gmail.com'
            receiver = [email]

            try:
                send_mail(subject, message, sender, receiver, fail_silently=False)
                messages.success(request, f"Enter the OTP sent to {email}")
                request.session['reset_email'] = email
                return redirect("reset_password_otp")
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
                messages.error(request, "Failed to send OTP email. Please try again later.")
                return render(request, 'doctors_template/password_reset.html', context)

        else:
            messages.error(request, f"{email} is not a registered doctor, Check the email and try again.")
            return render(request, 'doctors_template/password_reset.html', context)

    return render(request, 'doctors_template/password_reset.html')

# def password_reset(request):
#     if request.method == 'POST':
#         email= request.POST.get('email', '')
        
#         context ={
#             'email':email,
#         }
        
        
                
#         User = get_user_model()
#         if User.objects.filter(email=email).exists():
            
            
#             otp=OTP(email=email)
#             otp.save()
            
            
#             subject = "PASSWORD RESET OTP"
#             message = f"Your OTP for password reset is \n\n\n\n{otp.otp}."
#             sender = 'adeblessinme4u@gmail.com'
#             receiver = [email]
#             send_mail(subject, message, sender, receiver, fail_silently=True)

#             messages.success(request, f"Enter the OTP sent to {email}")
#             request.session['reset_email'] = email
#             return redirect("reset_password_otp")
#         else:
#             messages.error(request, f"{email}  is not a registered doctor, Check the email and try again.")
#             return render(request, 'doctors_template/password_reset.html', context)
        
        
#     return render(request, 'doctors_template/password_reset.html')


def reset_password_otp(request):
    if request.method == 'POST':
        otp_value = request.POST.get('otp')
        email = request.session.get('reset_email')

        otp_instance = OTP.objects.filter(otp=otp_value, email=email).first()
        if otp_instance:
            if otp_instance.is_expired():
                otp_instance.delete()
                messages.error(request, "The OTP has expired. Please request a new one.")
                return redirect('password_reset')
            else:
                return redirect('change_password')
        else:
            messages.error(request, "The OTP is not valid.")
            return redirect('reset_password_otp')

    return render(request, 'doctors_template/reset_password_otp.html')



def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        email = request.session.get('reset_email')
        
        if confirm_password != new_password:
            messages.error(request, "Password do not match!")
            return redirect('change_password')
        else:
            pass
        
        if email and confirm_password:
            User = get_user_model()
            user = User.objects.get(email=email)
            user.set_password(confirm_password)
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('doctor_login')
        
    return render(request, 'doctors_template/change_password.html')


def logout_doctor(request):
    logout(request) 
    return redirect('doctor_login')



