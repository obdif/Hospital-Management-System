from django.urls import path
from . import patient_views, doctor_views, views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # ========================== PATIENTS URL ==================

    path('', views.home, name="home"),
    
    
    path('patient/', patient_views.patient_dashboard, name="patient_dashboard"),
    path('patient/register/', patient_views.patient_register, name="patient_register"),
    path('patient/login/', patient_views.patient_login, name="patient_login"),
    path('patient/book_an_appointment/', patient_views.book_an_appointment, name="book_an_appointment"),
    path('patient/profile/', patient_views.patient_profile, name="patient_profile"),
    path('patient/doctors/', patient_views.doctors, name="patient_doctors"),
    path('patient/appointments/', patient_views.patient_appointments, name="patient_appointments"),
    path('patient/department/', patient_views.department, name="patient_departments"),
    path('patient/appointment_details/<int:appointment_id>/', patient_views.appointment_details, name="patient_appointment_details"),
    path('patient/medical_historys/', patient_views.medical_historys, name="medical_historys"),
    path('patient/medical_result_receipt/', patient_views.medical_result_receipt, name="medical_result_receipt"),
    path('patient/logout/', patient_views.logout_patient, name="patient_logout"),
    path('patient/edit_appointment/<int:appointment_id>/', patient_views.edit_appointment, name="edit_appointment"),
    path('patient/delete_appointment/<int:appointment_id>/', patient_views.delete_appointment, name="delete_appointment"),
    path('patient/patient_registration_confirmation/', patient_views.patient_registration_confirmation, name="patient_registration_confirmation"),
    path('fetch-available-times/', patient_views.fetch_available_times, name='fetch_available_times'),

    
    
    
    
    # ========================== DOCTORS URL ==================

    path('doctor/', doctor_views.doctor_dashboard, name="doctor_dashboard"),
    path('doctor/register/', doctor_views.doctor_register, name="doctor_register"),
    path('doctor/login/', doctor_views.doctor_login, name="doctor_login"),
    path('doctor/appointments/', doctor_views.doctor_appointments, name="doctor_appointments"),
    path('doctor/profile/', doctor_views.doctor_profile, name="doctor_profile"),
    path('doctor/doctors/', doctor_views.doctors, name="doctors"),
    path('doctor/invoices/', doctor_views.invoices, name="invoices"),
    path('doctor/invoices/create_invoice/', doctor_views.create_invoice, name="create_invoice"),
    path('doctor/invoices/create_invoice/<int:patient_id>/', doctor_views.create_invoice_with_patient, name="create_invoice_with_patient"),
    path('doctor/patients/', doctor_views.patients, name="doctor_patients"),
    path('doctor/departments/', doctor_views.department, name="doctor_department"),
    path('doctor/patients_details/<int:patient_id>/', doctor_views.patients_details, name="patients_details"),
    # path('doctor/patients_details/<str:patient_id>/', doctor_views.patients_details, name="patients_details"),
    path('doctor/add_patients/', doctor_views.add_patients, name="add_patients"),
    path('doctor/doctor_available/', doctor_views.doctor_available, name="doctor_available"),
    path('doctor/logout/', doctor_views.logout_doctor, name="doctor_logout"),
    path('doctor/appointments/accept/<int:appointment_id>/', doctor_views.accept_appointment, name="accept_appointment"),
    path('doctor/appointments/reject/<int:appointment_id>/', doctor_views.reject_appointment, name="reject_appointment"),
    path('doctor/appointments/appointment_details/<int:appointment_id>/', doctor_views.appointment_details, name="appointment_details"),


    path('doctor/search/', doctor_views.search_patients, name='search_patients'),
    # path('doctor/search/', doctor_views.patient_search, name='patient_search'),
    path('doctor/search_autocomplete/', doctor_views.search_autocomplete, name='search_autocomplete'),
    path('patient/search/', doctor_views.patient_search, name='patient_search'),


]








if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)