
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse


def homePage_main(request):
    return render(request,'index.html') #use html file -the first home page
    