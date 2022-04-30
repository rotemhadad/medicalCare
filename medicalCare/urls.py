#import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path as url
from medicalCare import views


urlpatterns = [
    url(r'^', include('doctor.urls')),
    path('admin/', admin.site.urls),
    #path('homepage/',include('homepage.urls')),
    path('doctor/',include('doctor.urls')),



]
