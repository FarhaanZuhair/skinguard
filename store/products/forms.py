from django import forms
from django.forms import ModelForm
from .models import Playerinfo, patient

class Playerform(ModelForm):
    class Meta:
        model = Playerinfo
        fields = '__all__'

class Patientform(ModelForm):
    class Meta:
        model = patient
        fields = '__all__'

class ImageUploadForm(forms.Form):
    image = forms.ImageField()