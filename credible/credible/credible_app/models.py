from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=200,primary_key=True)
    name = models.CharField(max_length=200)
    number_of_rating=models.IntegerField(default=0)
    weight=models.FloatField(default=1)



class WebsiteInfo(models.Model):
    name=models.CharField(max_length=200,primary_key=True)
    url=models.CharField(max_length=200)
    twitter=models.CharField(max_length=200,default='sample@twitter')
    wiki=models.CharField(max_length=200,default='sample@Wiki')
    location=models.CharField(max_length=200,default='sample@Headquaters')
    average=models.FloatField(default=0.0)
    average_media=models.FloatField(default=0.0)
    average_entertainment=models.FloatField(default=0.0)
    average_fact=models.FloatField(default=0.0)
    number_entertainment_reviews=models.IntegerField(default=0)
    number_media_reviews=models.IntegerField(default=0)
    number_fact_reviews=models.IntegerField(default=0)
    image = models.ImageField(upload_to='images', default='default.jpg')



class Review(models.Model):
    rating_choices = [
        ('News', 'News'),
        ('Entertainment', 'Entertainment'),
        ('Fact', 'Fact'),
        ('Overall', 'Overall'),
    ]
    email=models.ForeignKey(User , on_delete=models.CASCADE)
    website_name=models.ForeignKey(WebsiteInfo,on_delete=models.CASCADE)
    rating=models.IntegerField()
    comment=models.CharField(max_length=500)    
    category=models.CharField(choices=rating_choices,max_length=100)
    weight=models.IntegerField(default= 1)




