from urllib import request
from django.urls import path

from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

app_name = 'doctor'

urlpatterns = [

    path('', views.get_homePage, name='home'), 
    path('after_register',views.submit_Doctor, name = 'submit_Doctor'),
    path('homePage',views.Conect,name = 'Conect'),
    path('homePage/<int:user_id>',views.homePageD,name = 'homePageD'),
    path('homePage/patientQ/<int:user_id>',views.patientQ,name = 'patientQ'),
    #path('homePage/addPatientSucc/<int:user_id>',views.addPatientSucc,name = 'addPatientSucc'),


    

]
