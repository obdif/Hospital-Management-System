from django.urls import path
from .patient_views import * 
from .doctor_views import * 
from .views import *
# from opmApp.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # ========================== PATIENTS URL ==================

    path('', home, name="home"),
    
    
    path('patient/', patient_dashboard, name="patient_dashboard"),
    path('patient/register/', patient_register, name="patient_register"),
    path('patient/login/', patient_login, name="patient_login"),
    path('patient/book_an_appointment/', book_an_appointment, name="book_an_appointment"),
    path('patient/profile/', patient_profile, name="patient_profile"),
    path('patient/doctors/', patient_doctors, name="patient_doctors"),
    path('patient/appointments/', patient_appointments, name="patient_appointments"),
    path('patient/department/', patient_departments, name="patient_departments"),
    path('patient/appointment_details/<int:appointment_id>/', appointment_details, name="patient_appointment_details"),
    path('patient/medical_historys/', medical_historys, name="medical_historys"),
    path('patient/medical_result_receipt/<int:invoice_id>/', medical_result_receipt, name="medical_result_receipt"),
    path('patient/logout/', logout_patient, name="patient_logout"),
    path('patient/edit_appointment/<int:appointment_id>/', edit_appointment, name="edit_appointment"),
    path('patient/delete_appointment/<int:appointment_id>/', delete_appointment, name="delete_appointment"),
    path('patient/patient_registration_confirmation/', patient_registration_confirmation, name="patient_registration_confirmation"),
    path('fetch-available-times/', fetch_available_times, name='fetch_available_times'),
    path('patient/recover_id/', recover_id, name='recover_id'),

    
    
    
    
    # ========================== DOCTORS URL ==================

    path('doctor/', doctor_dashboard, name="doctor_dashboard"),
    path('doctor/register/', doctor_register, name="doctor_register"),
    path('doctor/login/', doctor_login, name="doctor_login"),
    path('doctor/appointments/', doctor_appointments, name="doctor_appointments"),
    path('doctor/profile/', doctor_profile, name="doctor_profile"),
    path('doctor/doctors/', doctors, name="doctors"),
    path('doctor/invoices/', invoices, name="invoices"),
    path('doctor/invoices/create_invoice/', create_invoice, name="create_invoice"),
    path('doctor/invoices/invoice_receipt/<int:invoice_id>/', invoice_receipt, name="invoice_receipt"),
    path('doctor/invoices/create_invoice/<int:patient_id>/', create_invoice_with_patient, name="create_invoice_with_patient"),
    path('doctor/patients/', patients, name="doctor_patients"),
    path('doctor/departments/', department, name="doctor_department"),
    path('doctor/patients_details/<int:patient_id>/', patients_details, name="patients_details"),
    path('doctor/add_patients/', add_patients, name="add_patients"),
    path('doctor/doctor_available/', doctor_available, name="doctor_available"),
    path('doctor/logout/', logout_doctor, name="doctor_logout"),
    path('doctor/appointments/accept/<int:appointment_id>/', accept_appointment, name="accept_appointment"),
    path('doctor/appointments/reject/<int:appointment_id>/', reject_appointment, name="reject_appointment"),
    path('doctor/appointments/appointment_details/<int:appointment_id>/', appointment_details, name="appointment_details"),
    path('doctor/invoices/edit_invoice/<int:invoice_id>/', edit_invoice, name="edit_invoice"),
    path('doctor/reset_password/', password_reset, name='password_reset'),
    path('doctor/reset_password_otp/', reset_password_otp, name='reset_password_otp'),
    path('doctor/search/', search_patients, name='search_patients'),
    path('doctor/search_autocomplete/', search_autocomplete, name='search_autocomplete'),
    path('patient/search/', patient_search, name='patient_search'),
    path('doctor/change_password/', change_password, name='change_password'),


]








if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)