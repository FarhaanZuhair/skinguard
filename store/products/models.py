from django.db import models
from users.models import UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import tensorflow as tf
import numpy as np
import os
from django.conf import settings



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
    
class YourModel(models.Model):
    # Your model fields

    @staticmethod
    def process_image(image):
        # Load the trained model
        model_path = os.path.join(settings.BASE_DIR, 'model', 'Mpox_Efficientnet_Model_New.h5')
        model = tf.keras.models.load_model(model_path)

        # Load and preprocess the image
        img = tf.keras.preprocessing.image.load_img(image, target_size=(300, 300))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, 0)  # Create a batch

        # Make predictions
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # Assuming you have a list of class names
        class_names = ['Monkeypox detected','Monkeypox not detected']
        predicted_class = class_names[np.argmax(score)]
        confidence = 100 * np.max(score)

        return predicted_class, confidence
    
    @staticmethod
    def process_skinimage(image):
        # Load the trained model
        model_path = os.path.join(settings.BASE_DIR, 'model', 'skin_cancer_detection_model_enb5.h5')
        model = tf.keras.models.load_model(model_path)

        # Load and preprocess the image
        img = tf.keras.preprocessing.image.load_img(image, target_size=( 456, 456))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, 0)  # Create a batch

        # Make predictions
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # Assuming you have a list of class names
        class_names = ['skin cancer detected','skin cancer not detected']
        predicted_class = class_names[np.argmax(score)]
        confidence = 100 * np.max(score)

        return predicted_class, confidence
    
    
    