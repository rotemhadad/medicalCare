from pickle import FALSE
from typing import List
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import manager
from django.db.models.fields import NullBooleanField
from django.db.models.query import QuerySet
from django.forms.formsets import formset_factory
from django.shortcuts import render,redirect,get_object_or_404 
from django.http import HttpResponse ,Http404
import openpyxl
from doctor.models import Doctor, Patient
from datetime import datetime,timedelta,date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging    
from django.contrib import messages
import re
from openpyxl import load_workbook
import datetime as dt
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings


# Create your views here.

def get_homePage(request):
    return render(request,'index.html') #use html file
    
def homePageD(request,user_id):
    doctor = Doctor.objects.get(user_id = user_id)
    return render(request,'home.html',{'doctor':doctor}) #use html file
    

def logout_user(request):
    logout(request)
    return redirect('/')

#register to Doctor 
def submit_Doctor(request):
    #list(messages.get_messages(request))
    user_id=request.POST.get('user_idup')
    name = request.POST.get('nameup')
    password = request.POST.get('passwordup')
    password2 = request.POST.get('password2up')

    if (password != password2):
        messages.error(request, 'ההרשמה לא בוצעה, אנא הזן בשנית סיסמאות תואמות')

    if (not checkPassword(password)): 
        messages.error(request, 'ההרשמה לא בוצעה, סיסמה לא תקינה')

    if (not checkName(name)): 
        messages.error(request, 'ההרשמה לא בוצעה, שם משתמש לא תקין')

    if (CheckIfDoctorExist(user_id,name)):
        messages.error(request, 'קיים משתמש בעל אותה ת"ז או שם משתמש, אנא נסה שנית')

    else:
        doctor = Doctor(user_id = user_id,name=name,password=password)
        doctor.save()
        messages.success(request, "משתמש נוצר בהצלחה!")

    return render(request,'index.html')



def checkPassword(password):
    if (len(password)<8 or len(password)>10):
        return False
    elif (not re.search("[a-z]", password) or not re.search("[A-Z]", password)):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[_@$]", password):
        return False
    else:
        return True

def checkName(name):
    if (len(name)<6 or len(name)>8):
        return False
    count = 0
    for c in name:
        if c.isdigit():
            count += 1
        elif not c.isalpha():
            return False
    if count>2:
        return False
    return True



#Checks the username and the password for sign in
def validateDoctor(name,password): 
    if name!= None and password!= None:
        for i in Doctor.objects.all():
            if i.name == name and i.password == password:
                return True
    return False


def Conect(request): #conect the doctor to homepage
    name = request.POST.get('namein')
    password = request.POST.get('passwordin')

    if validateDoctor(name,password):
       doctor = Doctor.objects.get(name = name,password = password)
       return render(request,'home.html',{'doctor':doctor})
    else:
        messages.error(request, 'שם משתמש וסיסמה אינם נכונים, אנא נסה שנית')
        return render(request,'index.html')




def index(request,user_id):
    doctor = Doctor.objects.get(user_id = user_id)
    if "GET" == request.method:
        return render(request, 'home.html', {'doctor':doctor})
    else:
        excel_file = request.FILES.get("excel_file",None)

        # you may put validations here to check extension or file size
        if (excel_file==None):
            return render(request, 'home.html', {'doctor':doctor})


        wb = openpyxl.load_workbook(excel_file)

        # getting all sheets
        sheets = wb.sheetnames
        print(sheets)

        # getting a particular sheet
        worksheet = wb["גיליון1"]
        print(worksheet)

        # getting active sheet
        active_sheet = wb.active
        print(active_sheet)

        # reading a cell
        print(worksheet["A1"].value)

        excel_data = list()
        # iterating over the rows and getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
                print(cell.value)
            excel_data.append(row_data)

        return render(request, 'home.html', {"excel_data":excel_data, 'doctor':doctor})

       


def CheckIfDoctorExist(user_id,name):
    for i in Doctor.objects.all():
        if i.user_id == user_id :
            return True
        if i.name == name:
            return True
    return False
         

def patientQ(request,user_id):
    doctor = Doctor.objects.get(user_id = user_id)
    patient_id=request.POST.get('patient_id')
    gender = request.POST.get("gender")
    smoke = request.POST.get("smoke")

    patient = Patient(patient_id=patient_id,gender=gender,smoke=smoke)
    patient.save()
    return render(request,'patientQ.html', {'doctor':doctor,'patient':patient})

def addPatientSucc(request,user_id):
    doctor = Doctor.objects.get(user_id = user_id)
    return render(request,'sucsees.html',{'doctor' :doctor})
