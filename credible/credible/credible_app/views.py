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
        print(user_email)
        print(User.objects.get(pk=user_email))
        five_star=[len(Review.objects.filter(website_name=website,rating=5,category='News')),len(Review.objects.filter(website_name=website,rating=5,category='Entertainment')),len(Review.objects.filter(website_name=website,rating=5,category='Fact'))]
        four_star=[len(Review.objects.filter(website_name=website,rating=4,category='News')),len(Review.objects.filter(website_name=website,rating=4,category='Entertainment')),len(Review.objects.filter(website_name=website,rating=4,category='Fact'))]
        three_star=[len(Review.objects.filter(website_name=website,rating=3,category='News')),len(Review.objects.filter(website_name=website,rating=3,category='Entertainment')),len(Review.objects.filter(website_name=website,rating=3,category='Fact'))]
        two_star=[len(Review.objects.filter(website_name=website,rating=2,category='News')),len(Review.objects.filter(website_name=website,rating=2,category='Entertainment')),len(Review.objects.filter(website_name=website,rating=2,category='Fact'))]
        one_star=[len(Review.objects.filter(website_name=website,rating=1,category='News')),len(Review.objects.filter(website_name=website,rating=1,category='Entertainment')),len(Review.objects.filter(website_name=website,rating=1,category='Fact'))]
        print('five_start',five_star)
        if 'rating' in request.POST:
            rc=Review.objects.filter(email=User.objects.get(pk=user_email),category=request.POST["type"],website_name=website)
            print("rc",rc)
            if(rc.count()==1):
                print("review exits")
                review=rc[0]
                review.rating=request.POST["rating"]
                review.comment=request.POST["comment"]
                review.save()
            else:
                print('new review')
                review = Review(email=User.objects.get(pk=user_email),website_name=website, rating=request.POST["rating"],comment=request.POST["comment"],category=request.POST["type"],weight=(User.objects.get(pk=user_email)).weight)
                review.save()
            
            updateCredibility(website,review)
        return render(request, 'reviewsite.html',{'website': website,'five':five_star,'four':four_star,'three':three_star,'two':two_star,'one':one_star})
    except WebsiteInfo.DoesNotExist:
        return render(request, 'addsite.html')

def addsite(request):
    is_added = 0
    if request.method == 'POST':
        print(request.POST)
        url = request.POST['url']
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print('Web site exists')
            else:
                print('Web site does not exist') 
                is_added = -1
        except:
            print("No response")
            is_added = -1
        if is_added == -1:
            return render(request, 'addsite.html',{'is_added':-1})
        web_name = request.POST['name']
        
        wiki = request.POST['wiki']
        twitter = request.POST['twitter']
        headquater = request.POST['headquater']

        new_web = WebsiteInfo(name=web_name,url=url,twitter=twitter,wiki=wiki, location=headquater)
        new_web.save()
        return render(request, 'index.html')
    else:
        return render(request, 'addsite.html')

def wantadd(request):
    return render(request, 'wantadd.html')

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
    reviews=Review.objects.all().filter(category=review.category)
    weight_sum=0
    for r in reviews:
        temp_user=r.email
        weight_sum=weight_sum+temp_user.weight
    print(weight_sum)
    if(review.category=='News'):
        print(review.rating)
        print(website.average_media)
        print('News Updated')
        new_media_average=float(float(website.average_media)*float(weight_sum-user.weight)
        + float(user.weight)*float(review.rating))/weight_sum
        website.number_media_reviews=website.number_media_reviews+1
        website.average_media=new_media_average
    elif(review.category=='Entertainment'):
        print('ENT Updated')
        new_entertainment_average=float(float(website.average_entertainment)*float(weight_sum-user.weight)
        + float(user.weight)*float(review.rating))/weight_sum
        website.number_entertainment_reviews=website.number_entertainment_reviews+1
        website.average_entertainment=new_entertainment_average
    
    elif(review.category=='Fact'):
        print('fact Updated')
        new_fact_average=float(float(website.average_fact)*float(weight_sum-user.weight)
        + float(user.weight)*float(review.rating))/weight_sum
        website.number_fact_reviews=website.number_fact_reviews+1
        website.average_fact=new_fact_average
    
    website.average=(website.average_entertainment+website.average_fact+website.average_media)/3
    website.save()
    


