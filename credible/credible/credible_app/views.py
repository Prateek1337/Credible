from django.shortcuts import render
from django.http import HttpResponse
import os
import requests

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
