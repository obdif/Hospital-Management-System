from django import forms

class PatientSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=True, label='Search for Patient (Name, ID, or Email)')
