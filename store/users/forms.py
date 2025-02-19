from django import forms
from .models import Diagnosis

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['first_name', 'last_name', 'address', 'symptoms', 'disease_image']