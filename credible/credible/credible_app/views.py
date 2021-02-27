from django.http import HttpResponse,Http404
import os
import requests
from .models import WebsiteInfo, User, Review
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
user_email="test"
def index(request):
    print(user_email)
    return render(request, 'index.html')

def reviewsite(request):
    global user_email
    print(user_email)
    print(request.POST)
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
    
    # print(WebsiteInfo.objects.get(pk=search_key))
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
            global user_email
            user_email=request.POST['email']
            return render(request,'index.html')
        except:
            print("ok")
            return render(request, 'login.html')
    return render(request, 'login.html')



def updateCredibility(website,review):
    user=User.objects.get(pk = user_email)
    reviews=Review.objects.query(category=review.category)
    weight_sum=0
    for r in reviews:
        temp_user=User.objects.get(pk=r.email)
        weight_sum=weight_sum+temp_user.weight

    if(review.category=='News'):
        print('News Updated')
        new_media_average=(website.average_media*(weight_sum-user.weight)+user.weight*review.rating)/(weight_sum)
        website.number_media_reviews=website.number_media_reviews+1
        website.average_media=new_media_average
    elif(review.category=='Entertainment'):
        print('ENT Updated')
        new_entertainment_average=(website.average_entertainment*website.number_entertainment_reviews+user.weight*review.rating)/(website.number_entertainment_reviews+1)
        website.number_entertainment_reviews=website.number_entertainment_reviews+1
        website.average_entertainment=new_entertainment_average
    
    elif(review.category=='Fact'):
        print('fact Updated')
        new_fact_average=(website.average_fact*website.number_fact_reviews+user.weight*review.rating)/(website.number_fact_reviews+1)
        website.number_fact_reviews=website.number_fact_reviews+1
        website.average_fact=new_fact_average
    
    website.average=(website.average_entertainment+website.average_fact+website.average_media)/3
    website.save()
    


