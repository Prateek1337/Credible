from django.shortcuts import render,redirect
from django.http import HttpResponse
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def reviewsite(request):
    search_key = request.POST['search']
    try:
        response = requests.get(search_key)
        if response.status_code == 200:
            print('Web site exists')
        else:
            print('Web site does not exist') 
    except:
        print("No response")
    return render(request, 'reviewsite.html')

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
