from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checksite',views.reviewsite),
    path('signup',views.signup),
    path('login',views.login)
]
