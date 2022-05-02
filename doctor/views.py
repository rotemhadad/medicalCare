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
from doctor.models import BloodTest, Doctor, Patient
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




def excelUpload(request,user_id):
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
        print(worksheet["A1"].value) #print in terminal

        excel_data = list()
        # iterating over the rows and getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
                print(cell.value)
            excel_data.append(row_data)

        return render(request, 'patientQ.html', {"excel_data":excel_data, 'doctor':doctor})

       


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
    age = request.POST.get("age")
    name = request.POST.get("name")
    lastName = request.POST.get("lastName")
    smoke = request.POST.get("smoke")
    medicine = request.POST.get("medicine")
    eastCommunity = request.POST.get("eastCommunity")
    ethiopian = request.POST.get("ethiopian")
    pregnancy = request.POST.get("pregnancy")
    lst=[smoke,medicine,eastCommunity,ethiopian,pregnancy]
    for i in lst:
        if (i=="True"):
            i=True
        else:
            i=False
            
    #excel file
    bloodTest=BloodTest(WBC=None,Neut=None,Lymph=None,RBC=None,HCT=None,Urea=None,Hb=None,Crtn=None,Iron=None,HDL=None,AP=None)


    excel_file = request.FILES.get("excel_file",None)
    excel_data=None
    if (excel_file!=None):
        wb = openpyxl.load_workbook(excel_file)
        # getting all sheets
        sheets = wb.sheetnames
        print(sheets)

        # getting a particular sheet
        worksheet = wb["גיליון1"]
        # print(worksheet)

        # getting active sheet
        active_sheet = wb.active
        # print(active_sheet)

        WBC = worksheet["B1"].value
        Neut = worksheet["B2"].value
        Lymph = worksheet["B3"].value  
        RBC = worksheet["B4"].value  
        HCT = worksheet["B5"].value  
        Urea = worksheet["B6"].value  
        Hb = worksheet["B7"].value  
        Crtn = worksheet["B8"].value         
        Iron = worksheet["B9"].value  
        HDL = worksheet["B10"].value  
        AP = worksheet["B11"].value  
        
        bloodTest=BloodTest(WBC=WBC,Neut=Neut,Lymph=Lymph,RBC=RBC,HCT=HCT,Urea=Urea,Hb=Hb,Crtn=Crtn,Iron=Iron,HDL=HDL,AP=AP)
        
    else:
        WBC = request.POST.get('WBC')
        Neut = request.POST.get('Neut')
        Lymph = request.POST.get('Lymph') 
        RBC = request.POST.get('RBC')
        HCT = request.POST.get('HCT')
        Urea = request.POST.get('Urea') 
        Hb = request.POST.get('Hb')
        Crtn = request.POST.get('Crtn')       
        Iron = request.POST.get('Iron')
        HDL = request.POST.get('HDL')
        AP = request.POST.get('AP')
        if(WBC=="" or Neut=="" or Lymph=="" or RBC=="" or HCT=="" or Urea=="" or
            Hb=="" or Crtn=="" or Iron=="" or HDL=="" or AP==""):
                messages.error(request, 'אנא מלא את כל הערכים')

        else:
            bloodTest=BloodTest(WBC=WBC,Neut=Neut,Lymph=Lymph,RBC=RBC,HCT=HCT,Urea=Urea,Hb=Hb,Crtn=Crtn,Iron=Iron,HDL=HDL,AP=AP)
    bloodTest.save()
    patient = Patient(patient_id=patient_id, name=name, lastName= lastName,gender=gender,age=age,
    smoke=smoke, pregnancy=pregnancy, ethiopian=ethiopian, eastCommunity=eastCommunity,bloodTest=bloodTest)
    patient.save()
    return render(request,'patientQ.html', {'doctor':doctor,'patient':patient})





def addPatientSucc(request,user_id):
    doctor = Doctor.objects.get(user_id = user_id)
    return render(request,'sucsees.html',{'doctor' :doctor})
