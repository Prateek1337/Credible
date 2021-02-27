from django.shortcuts import render
from django.http import HttpResponse,Http404
import os
import requests
from .models import WebsiteInfo

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

def signup(request):
    return render(request,'signup.html')

def login(request):
    return render(request, 'login.html')
