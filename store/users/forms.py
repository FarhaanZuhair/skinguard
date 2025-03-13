from django import forms
from .models import Diagnosis, SkinDiagnosis

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['first_name', 'last_name', 'address', 'symptoms', 'disease_image']
class SkinDiagnosisForm(forms.ModelForm):
    class Meta:
        model = SkinDiagnosis
        fields = ['first_name', 'last_name', 'address', 'symptoms', 'disease_image']    