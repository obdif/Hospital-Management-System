from django.contrib.auth.backends import BaseBackend
from .models import Patient

class PatientBackend(BaseBackend):

    def authenticate(self, request, username=None, **kwargs):
        try:
            patient = Patient.objects.get(patient_id__iexact=username)  # Case insensitive match
            return patient
        except Patient.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Patient.objects.get(pk=user_id)
        except Patient.DoesNotExist:
            return None
