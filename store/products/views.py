from django.shortcuts import render, get_object_or_404,redirect
from . models import Playerinfo,patient
from . forms import Playerform,Patientform
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
from store.model_loader import predict_disease
import os
from django.conf import settings

def disease_detection(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            predicted_class, confidence = predict_disease(image_path)
            return JsonResponse({'predicted_class': predicted_class, 'confidence': confidence})

    else:
        form = ImageUploadForm()
    return render(request, 'model/disease_detection.html', {'form': form})

genai.configure(api_key="AIzaSyDepoMb98fI91dnQFBpUABAYs1WQLgjA8c")

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_text = data.get("query")

            conversation = [{'role': 'user', 'parts': [user_text]}]
            response = model.generate_content(conversation, stream=True)

            # Concatenate and format response
            response_text = "".join([chunk.text for chunk in response])

            return JsonResponse({"response": response_text})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"response": "Sorry, I couldn't process your request at the moment."})
    else:
        return render(request, 'frontend/chatbot.html')

def showproducts(request):

    obj=Playerinfo.objects.filter(fav_club__preclub='sporting')
    print(obj)
    return render(request,"products.html",{'a1':obj})
def dash(request):
    pf=Playerform
    if request.POST:
        pf=Playerform(request.POST)
        if pf.is_valid:
            pf.save()
        else:
            pf=Playerform()    
    return render(request,'dash.html',{'pf':pf})
def list(request):
    recent_visit=request.session.get('recent_visit',[])
    count=request.session.get('count',0)
    count=int(count)
    count=count+1
    request.session['count']=count
    recent_visit_player=Playerinfo.objects.filter(pk__in=recent_visit)
    obj=Playerinfo.objects.all()
    print(obj)
    # return render(request,"products.html",{'a1':obj})
    pf=Playerform
    if request.POST:
        pf=Playerform(request.POST,request.FILES)
        print(request.FILES)
        if pf.is_valid:
            pf.save()
            return redirect('list')
        else:

            print(pf.errors)
            pf=Playerform()    
    return render(request,'list.html',{'pf':pf,'a1':obj,'count':count,'recent_player':recent_visit_player})



def edit(request, pk):
    instance_edit = get_object_or_404(Playerinfo, pk=pk)
    if request.method == 'POST':
        frm = Playerform(request.POST, request.FILES, instance=instance_edit)
        if frm.is_valid():
            frm.save()
            return redirect('list')
    else:
        recent_visit=request.session.get('recent_visit',[])
        recent_visit.insert(0,pk)
        request.session['recent_visit']=recent_visit
        frm = Playerform(instance=instance_edit)
    return render(request, 'edit.html', {'pf': frm})


def delete(request,pk):
    instance=Playerinfo.objects.get(pk=pk)
    instance.delete()
    obj=Playerinfo.objects.all()
    return render(request,'list.html',{'a1':obj})


def list_view(request, pk):
    obj = get_object_or_404(Playerinfo, pk=pk)
    return render(request, 'list.html', {'obj': obj})
def patients(request):
    pf=Patientform
    if request.POST:
        pf=Patientform(request.POST,request.FILES)
        print(request.FILES)
        if pf.is_valid:
            pf.save()
            return redirect('patientlist')
        else:
            print(pf.errors)
    else:
        pf=Patientform()
    return render(request,'patient.html',{'pf':pf})
def patientlist(request):
    form=patient.objects.all()
    print(form)
    return render(request,'patientlist.html',{'form':form})
def edit1(request, pk):
    instance_edit1 = get_object_or_404(patient,pk=pk)
    if request.POST:
        frm = Patientform(request.POST, request.FILES, instance=instance_edit1)
        if frm.is_valid():
            frm.save()
            return redirect('patientlist')
    else:
        frm = Patientform(instance=instance_edit1)
    return render(request, 'edit1.html', {'pf': frm})

def delete1(request,pk):
    instance=patient.objects.get(pk=pk)
    instance.delete()
    obj=patient.objects.all()
    return render(request,'patientlist.html',{'form':obj})
def report(request,pk):
    instance_rep = get_object_or_404(patient,pk=pk)
    # obj=patient.objects.filter(pk=pk)
    return render(request,'report.html',{'element':instance_rep})

def home(request):
    return render(request, 'frontend/home.html')
def about(request):
    return render(request, 'frontend/about.html')

