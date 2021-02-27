from django.http import HttpResponse,Http404
import os
import requests
from .models import WebsiteInfo, User
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def reviewsite(request):
    search_key = request.POST['search']
    url='https://www.'+search_key+'.com'
    print(search_key)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('Web site exists')
        else:
            print('Web site does not exist') 
    except:
        print("No response")
        return HttpResponse("No response from website")
    
    print(WebsiteInfo.objects.get(pk=search_key))
    try:
        website=WebsiteInfo.objects.get(pk=search_key)
        return render(request, 'reviewsite.html',{'website': website})
    except WebsiteInfo.DoesNotExist:
        return HttpResponse("Website does not exist  in database")

@csrf_exempt
def signup(request):
    
    if request.method == "POST":
        #context = {"name":"hehe", "email":"ee", "password":"11"}
        print(request.POST)
        try: 
            User.objects.get(email = request.POST["email"])
            return render(request,'signup.html')
        except:
            user = User(name=request.POST["name"],email=request.POST["email"])
            user.save()
            return render(request,"index.html")
    return render(request,'signup.html')

@csrf_exempt
def login(request):
    print(request)
    if request.method == "POST":
        try: 
            print(request.POST)
            User.objects.get(email = request.POST["email"])
            return render(request,'index.html')
        except:
            print("ok")
            return render(request, 'login.html')
    return render(request, 'login.html')
