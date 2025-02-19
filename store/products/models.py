from django.db import models
from users.models import UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class patient(models.Model):
    name = models.CharField(max_length=250)
    age = models.IntegerField()
    address = models.CharField(max_length=250)
    disease_pic = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.name

class Coach(models.Model):
    name= models.CharField(max_length=255)
    def __str__(self):
        return self.name


class playerhistory(models.Model):
    preclub = models.CharField(max_length=250)
    current_club = models.CharField(max_length=25)
    def __str__(self):
        return self.preclub

class transferfee(models.Model):
    fee= models.CharField(max_length=20) 
    def __str__(self):
        return self.fee
   
class Playerinfo(models.Model):
    name = models.CharField(max_length=250)
    club = models.CharField(max_length=25)
    position = models.CharField(max_length=30)
    poster = models.ImageField(upload_to='images/')
    transferfees=models.ManyToManyField(transferfee,related_name='fee_paid')
    fav_club= models.OneToOneField(playerhistory, on_delete=models.SET_NULL,null=True,related_name='playerinfo_fav_club')
    rumor= models.ForeignKey(Coach,on_delete=models.CASCADE,null=True,related_name='playerinfo_rumor')
    def __str__(self):
        return self.name
    
        
