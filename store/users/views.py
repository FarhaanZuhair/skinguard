from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile

from .models import Diagnosis, SkinDiagnosis
from .forms import DiagnosisForm, SkinDiagnosisForm
import random
import os
from products.models import YourModel  # Replace 'your_model_module' with the actual module name
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import SkinDiagnosis
import requests


# Create your views here.
def reporthistory(request):
    return render(request,'users/reporthistory.html')
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

@login_required
def skin_cancer_diagnose(request):
    if request.method == 'POST':
        form = SkinDiagnosisForm(request.POST, request.FILES)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.user = request.user
            diagnosis.save()
            return redirect('view_skin_diagnosis', pk=diagnosis.pk)
    else:
        form = SkinDiagnosisForm()
    return render(request, 'users/skincancerdiagnose.html', {'form': form})

# @login_required
# def view_skin_diagnosis(request, pk):
#     diagnosis = get_object_or_404(SkinDiagnosis, pk=pk)

#     if diagnosis.disease_image:
#         # Process the uploaded image
#         predicted_class, confidence = YourModel.process_skinimage(diagnosis.disease_image.path)
#         diagnosis_result = f"{predicted_class} with {confidence:.2f}% confidence"
#     else:
#         diagnosis_result = "No image uploaded"

#     return render(request, 'users/view_skin_diagnosis.html', {'diagnosis': diagnosis, 'diagnosis_result': diagnosis_result})

@login_required
def view_skin_diagnosis(request, pk):
    diagnosis = get_object_or_404(SkinDiagnosis, pk=pk)

    if diagnosis.disease_image:
        # Process the uploaded image
        predicted_class, confidence = YourModel.process_skinimage(diagnosis.disease_image.path)
        diagnosis_result = f"{predicted_class} with {confidence:.2f}% confidence"
        # Generate the report and save it to a file
        report_path = generate_report(diagnosis, diagnosis_result)


        # Upload image to IPFS and get CID
        cid = upload_to_ipfs(report_path)
        # Save the CID and diagnosis result to the database
        # diagnosis.cid = cid
        # diagnosis.diagnosis_result = diagnosis_result
        # diagnosis.save()

    else:
        diagnosis_result = "No image uploaded"
        cid = None

    return render(request, 'users/view_skin_diagnosis.html', {'diagnosis': diagnosis, 'diagnosis_result': diagnosis_result, 'cid': cid})

def upload_to_ipfs(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": settings.PINATA_API_KEY,
        "pinata_secret_api_key": settings.PINATA_SECRET_API_KEY,
    }
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={"file": file}, headers=headers)
    if response.status_code == 200:
        return response.json().get('IpfsHash')
    else:
        return None
    
def generate_report(diagnosis, diagnosis_result):
    report_content = f"""
    Diagnosis Report
    ----------------
    Name: {diagnosis.first_name} {diagnosis.last_name}
    Address: {diagnosis.address}
    Symptoms: {diagnosis.symptoms}
    Diagnosis Result: {diagnosis_result}
    Report Date: {diagnosis.report_date}
    """
    report_path = os.path.join(settings.MEDIA_ROOT, f'reports/{diagnosis.pk}_report.txt')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as report_file:
        report_file.write(report_content)
    return report_path
