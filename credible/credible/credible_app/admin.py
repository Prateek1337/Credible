from django.contrib import admin
from .models import  User,WebsiteInfo,Review


# Register your models here.

admin.site.register(User)
admin.site.register(WebsiteInfo)
admin.site.register(Review)

