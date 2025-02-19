from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Diagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    symptoms = models.TextField()
    disease_image = models.ImageField(upload_to='disease_images/')
    report_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis for {self.first_name} {self.last_name} on {self.report_date}"    