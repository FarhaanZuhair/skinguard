from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import Diagnosis
from .forms import DiagnosisForm
import random
import os
from products.models import YourModel  # Replace 'your_model_module' with the actual module name



from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

# Create your views here.
def logout(request):
    auth_logout(request)
    return redirect('login')

def login(request):
    error_message=None
    user=None
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            auth_login(request,user)
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
            return redirect('profilepage', pk=user.pk)
        else:  
            error_message='Invalid username or password'
    return render(request,'users/login.html',{'error_message':error_message,'user':user})

def signup(request):
    user=None
    error_message=None
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=User.objects.create_user(username=username,password=password)
            return redirect('profilepage', pk=user.pk)
        except Exception as e:
            error_message=str(e)
    return render(request,'users/create.html',{'user':user,'error_message':error_message})
# def profilepage(request,username):
#     username=User.objects.get(username=username)
#     details=username.playerinfo_set.all()
#     return render(request,'users/profilepage.html',{'username':username,'details':details})

# @login_required
# def profilepage1(request):
#     username= User.objects.get(username=request.user)
#     return render(request, 'users/profilepage.html',{ 'username':username})

@login_required
def profilepage(request, pk):
    user_profile = UserProfile.objects.get(user__pk=pk)
    return render(request, 'users/profilepage.html', {'details': user_profile})


@login_required
def edit_profile(request, pk):
    user_profile = UserProfile.objects.get(user__pk=pk)
    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile_pic = request.FILES.get('profile_pic')
        user_profile.bio = bio
        if profile_pic:
            user_profile.profile_pic = profile_pic
        user_profile.save()
        return redirect('profilepage', pk=user_profile.user.pk)
    return render(request, 'users/profilepage.html', {'details': user_profile})


@login_required
def diagnose(request):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST, request.FILES)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.user = request.user
            diagnosis.save()
            return redirect('view_diagnosis', pk=diagnosis.pk)
    else:
        form = DiagnosisForm()
    return render(request, 'users/diagnose.html', {'form': form})

@login_required
def view_diagnosis(request, pk):
    diagnosis = get_object_or_404(Diagnosis, pk=pk)

    if diagnosis.disease_image:
        # Process the uploaded image
        predicted_class, confidence = YourModel.process_image(diagnosis.disease_image.path)
        diagnosis_result = f"{predicted_class} with {confidence:.2f}% confidence"
    else:
        diagnosis_result = "No image uploaded"

    return render(request, 'users/view_diagnosis.html', {'diagnosis': diagnosis, 'diagnosis_result': diagnosis_result})