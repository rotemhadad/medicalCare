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
import simplejson as json

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
    if (age!= None):
        diagnose(bloodTest,patient,int(age))
    return render(request,'patientQ.html', {'doctor':doctor,'patient':patient})



def addPatientSucc(request,user_id):
    doctor = Doctor.objects.get(user_id = user_id)
    return render(request,'sucsees.html',{'doctor' :doctor})

def diagnose(bloodtest,patient,age):
    count=0
    if (patient.medicine == True):
        count = 1
    anemia  = ".אנמיה- שני כדורי 10 מג של בי12 ביום למשך חודש"
    diet = ".דיאטה- לתאם פגישה עם תזונאי"
    bleading = ".דימום- להתפנות בדחיפות לבית החולים"
    hiperlipidemia = ".היפרליפידמיה(שומנים בדם)- של לתאם פגישה עם תזונאי, כדור 5 מג של סימוביל ביום למשך שבוע"
    disruptionOfBlood = ".הפרעה ביצירת הדם\תאי הדם - כדור 10 מג של בי12 ביום למשך חודש וכדור 5 מג של חומצה פולית ביום למשך חודש"
    hematologicalDisorder = ".הפרעה המטולוגיה- זריקה של הורמון לעידוד ייצור תאי הדם האדומים"
    ironPoisoning= ".הרעלת ברזל - להתפנות לבית החולים"
    dehydration = ".התייבשות- מנוחה מוחלטת בשכיבה, החזרת נוזלים בשתייה"
    infection = ".זיהום- אנטיביוטיקה ייעודית"
    vitaminDef = ".חוסר בוויטמינם- הפנייה לבדיקת דם לזיהוי הוויטמינים החסרים"
    viralDisease = ".מחלה ויראלית- לנוח בבית"
    diseaseInBile = ".מחלות בדרכי המרה- הפנייה לטיפול כירורגי"
    heartDisease = ".מחלות לב - לתאם פגישה עם תזונאי"
    bloodDisease = ".מחלת דם- שילוב של ציקלופוספאמיד וקורטיקוסרואידים"
    liverDisease = ".מחלת כבד- הפנייה לאבחנה ספציפית לצורך קביעת טיפול"
    kidneyDisease = ".מחלת כליה - איזון את רמות הסוכר בדם"
    ironDef = ".מחסור בברזל - שני כדורי 10 מג של בי12 ביום למשך חודש"
    muscleDisease = ".מחלות שריר- שני כדורי 5 מג של כורכום סי3 של אלטמן ביום למשך חודש"
    smokeing = ".מעשנים- להפסיק לעשן"
    lungDisease = ".מחלת ריאות- להפסיק לעשן / הפנייה לצילום רנטגן של הריאות"
    overactiveThyroid = "Propylthiouracil פעילות יתר של בלוטת התריס- להקטנת פעילות בלוטת התריס"
    adultDiabetes = ".סוכרת מבוגרים- התאמת אינסולין למטופל"
    cancer = " אנטרקטיניב - Entrectinibסרטן -"
    meatInc = ".צריכה מוגברת של סרטן- לתאם פגישה עם תזונאי"
    variousMedications = ".שימוש בתרופות שונות- הפנייה לרופא המשפחה לצורך בדיקת התאמה בין התרופות"
    malnutrition = ".תת תזונה- לתאם פגישה עם תזונאי"

    #WBC check
    if (age!=None):
        if (age>=0 and age<=3):
            if (int(bloodtest.WBC)<6000):
                patient.diagnose=json.dumps("ערכים נמוכים של כמות תאי הדם הלבנים הכללית מצביעים על מחלה ויראלית, כשל של מערכת החיסון ובמקרים נדירים ביותר על סרטן.",ensure_ascii=False)
                patient.treatment=json.dumps(viralDisease,ensure_ascii=False)
                patient.treatment=json.dumps(cancer,ensure_ascii=False)
                patient.treatment=json.dumps(bloodDisease,ensure_ascii=False)
            if (int(bloodtest.WBC)>17500):
                patient.diagnose=json.dumps(" ערכים גבוהים של כמות תאי הדם הלבנים הכללית מצביעים לרוב על קיומו של זיהום, אם קיימת מחלת חום. במקרים אחרים, נדירים ביותר, עלולים ערכים גבוהים מאוד להעיד על מחלת דם או סרטן. ",ensure_ascii=False)
                patient.treatment=json.dumps(infection,ensure_ascii=False)
                patient.treatment=json.dumps(bloodDisease,ensure_ascii=False)
                patient.treatment=json.dumps(cancer,ensure_ascii=False)
        elif (age>3 and age<=17):
            if (int(bloodtest.WBC)<5500):
                patient.diagnose=json.dumps("ערכים נמוכים של כמות תאי הדם הלבנים הכללית מצביעים על מחלה ויראלית, כשל של מערכת החיסון ובמקרים נדירים ביותר על סרטן.",ensure_ascii=False)
                patient.treatment=json.dumps(viralDisease,ensure_ascii=False)
                patient.treatment=json.dumps(cancer,ensure_ascii=False)
                patient.treatment=json.dumps(bloodDisease,ensure_ascii=False)            
            if (int(bloodtest.WBC)>15500):
                patient.diagnose=json.dumps(" ערכים גבוהים של כמות תאי הדם הלבנים הכללית מצביעים לרוב על קיומו של זיהום, אם קיימת מחלת חום. במקרים אחרים, נדירים ביותר, עלולים ערכים גבוהים מאוד להעיד על מחלת דם או סרטן. ",ensure_ascii=False)
                patient.treatment=json.dumps(infection,ensure_ascii=False)
                patient.treatment=json.dumps(bloodDisease,ensure_ascii=False)
                patient.treatment=json.dumps(cancer,ensure_ascii=False)
        else:
            if (int(bloodtest.WBC)<4500):
                patient.diagnose=json.dumps("ערכים נמוכים של כמות תאי הדם הלבנים הכללית מצביעים על מחלה ויראלית, כשל של מערכת החיסון ובמקרים נדירים ביותר על סרטן.",ensure_ascii=False)
                patient.treatment=json.dumps(viralDisease,ensure_ascii=False)
                patient.treatment=json.dumps(cancer,ensure_ascii=False)
                patient.treatment=json.dumps(bloodDisease,ensure_ascii=False)         
            if (int(bloodtest.WBC)>11000):
                patient.diagnose=json.dumps(" ערכים גבוהים של כמות תאי הדם הלבנים הכללית מצביעים לרוב על קיומו של זיהום, אם קיימת מחלת חום. במקרים אחרים, נדירים ביותר, עלולים ערכים גבוהים מאוד להעיד על מחלת דם או סרטן. ",ensure_ascii=False)
                patient.treatment=json.dumps(infection,ensure_ascii=False)
                patient.treatment=json.dumps(bloodDisease,ensure_ascii=False)
                patient.treatment=json.dumps(cancer,ensure_ascii=False)
    #Neut check
    if(int(bloodtest.Neut)<28):
        patient.diagnose=json.dumps(" ערכים נמוכים בכמות תאי הדם הלבנים האחראים בעיקר על חיסול החיידקים- מעידים על הפרעה ביצירת הדם, על נטייה לזיהומים מחיידקים ובמקרים נדירים - על תהליך סרטני.",ensure_ascii=False)
        patient.treatment=json.dumps(disruptionOfBlood,ensure_ascii=False)
        patient.treatment=json.dumps(cancer,ensure_ascii=False)
        patient.treatment=json.dumps(infection,ensure_ascii=False)     #כתוב רק נטייה לזיהום         
        count=count+3
    if(int(bloodtest.Neut)>54):
        patient.diagnose=json.dumps("ערכים גבוהים בכמות תאי הדם הלבנים האחראים בעיקר על חיסול החיידקים מעידים על זיהום חיידקי.",ensure_ascii=False)
        patient.treatment=json.dumps(infection,ensure_ascii=False)        
        count=count+1
    #Lymph check
    if(int(bloodtest.Lymph)<36):
        patient.diagnose=json.dumps(" ערכים נמוכים תאי דם לבנים האחראים על הריגת נגיפים או חיידקים הנמצאים בגוף זמן ממושך מעידים על בעיה ביצירת תאי דם ",ensure_ascii=False)
        patient.treatment=json.dumps(disruptionOfBlood,ensure_ascii=False)
        count=count+2
    if(int(bloodtest.Lymph)>52):    
        patient.diagnose=json.dumps("ערכים גבוהים בתאי דם לבנים האחראים על הריגת נגיפים או חיידקים הנמצאים בגוף זמן ממושך עשויים להצביע על זיהום חידקי ממושך או על סרטן הלימפומה",ensure_ascii=False)        
        patient.treatment=json.dumps(infection,ensure_ascii=False)
        patient.treatment=json.dumps(cancer,ensure_ascii=False)
    #RBC check
    if(int(bloodtest.RBC)<4.5):
        patient.diagnose=json.dumps(" ערכים נמוכים בכדוריות הדם האדומות אחראיות על קשירת חמצן מהריאות, על הובלתו לרקמות הגוף, על קליטת פחמן דו-חמצנימתאי הגוף השונים ועל פליטתו בחזרה לריאות - עלולים להצביע על אנמיה או על דימומים קשים. ",ensure_ascii=False)
        patient.treatment=json.dumps(anemia,ensure_ascii=False)
        patient.treatment=json.dumps(bleading,ensure_ascii=False)
    if(int(bloodtest.RBC)>6):    
        patient.diagnose=json.dumps(" ערכים נמוכים בכדוריות הדם האדומות אחראיות על קשירת חמצן מהריאות, על הובלתו לרקמות הגוף, על קליטת פחמן דו-חמצנימתאי הגוף השונים ועל פליטתו בחזרה לריאות -  עלולים להצביע על הפרעה במערכת ייצור הדם. רמות גבוהות נצפו גם אצל מעשנים ואצל חולים במחלות ריאות.",ensure_ascii=False)
        patient.treatment=json.dumps(lungDisease,ensure_ascii=False)
        patient.treatment=json.dumps(disruptionOfBlood,ensure_ascii=False)
        if (patient.smoke == True):
            patient.treatment=json.dumps(smokeing,ensure_ascii=False)
    #HCT check
    if(patient.gender == "woman"):
        if (int(bloodtest.HCT)<33):
            patient.diagnose=json.dumps(" ערכים נמוכים בנפח כדוריות הדם האדומות בתוך כלל נוזל הדם. - מצביעים לרוב על דימום או על אנמיה ",ensure_ascii=False)
            patient.treatment=json.dumps(anemia,ensure_ascii=False)
            patient.treatment=json.dumps(bleading,ensure_ascii=False)
        if (int(bloodtest.HCT)>47):
            patient.diagnose=json.dumps(" ערכים נמוכים בנפח כדוריות הדם האדומות בתוך כלל נוזל הדם. - שכיח בדרך כלל אצל מעשנים.  ",ensure_ascii=False)
        if (patient.smoke == True):
            patient.treatment=json.dumps(smokeing,ensure_ascii=False)
    if(patient.gender == "man"):
        if (int(bloodtest.HCT)<37):
            patient.diagnose=json.dumps(" ערכים נמוכים בנפח כדוריות הדם האדומות בתוך כלל נוזל הדם. - מצביעים לרוב על דימום או על אנמיה ",ensure_ascii=False)
            patient.treatment=json.dumps(anemia,ensure_ascii=False)
            patient.treatment=json.dumps(bleading,ensure_ascii=False)
        if (int(bloodtest.HCT)>54):
            patient.diagnose=json.dumps(" ערכים נמוכים בנפח כדוריות הדם האדומות בתוך כלל נוזל הדם. - שכיח בדרך כלל אצל מעשנים.  ",ensure_ascii=False)
        if (patient.smoke == True):
            patient.treatment=json.dumps(smokeing,ensure_ascii=False)

    #Urea check
    if((patient.eastCommunity == False and int(bloodtest.Urea)<17) or (patient.eastCommunity == True and int(bloodtest.Urea)<18.7)):
        patient.diagnose=json.dumps("ערכים נמוכים ברמת השתנן בדם. שתנן הוא התוצר הסופי של תהליך חילוף החומרים של חלבונים בגוף- עלול להצביע על: תת תזונה, דיאטה דלת חלבון או מחלת כבד.",ensure_ascii=False)
        if(patient.pregancy == True):
            patient.diagnose=json.dumps("המטופלת בהריון - נא לשים לב בהריון רמת השתנן יורדת.",ensure_ascii=False)
        patient.treatment=json.dumps(malnutrition,ensure_ascii=False)
        patient.treatment=json.dumps(diet,ensure_ascii=False)
        patient.treatment=json.dumps(liverDisease,ensure_ascii=False)
    if((patient.eastCommunity == False and int(bloodtest.Urea)>43) or (patient.eastCommunity == True and int(bloodtest.Urea)>47.3)):
        patient.diagnose=json.dumps(" ערכים גבוהים ברמת השתנן בדם. שתנן הוא התוצר הסופי של תהליך חילוף החומרים של חלבונים בגוף - עלולים להצביע על מחלות כליה,התייבשות או דיאטה עתירת חלבונים",ensure_ascii=False)
        patient.treatment=json.dumps(kidneyDisease,ensure_ascii=False)
        patient.treatment=json.dumps(dehydration,ensure_ascii=False)
        patient.treatment=json.dumps(diet,ensure_ascii=False)


    #HB check
    if((patient.gender == "woman" and age >17 and int(bloodtest.Hb)<12) or (patient.gender == "man" and age >17 and int(bloodtest.Hb)<12) or (age <=17 and int(bloodtest.Hb)<11.5)):
        patient.diagnose=json.dumps("ערכים נמוכים ברמת ההמוגלובין- המוגלובין הוא מרכיב בתוך הכדורית האדומה, אשר אחראי על קשירתם ועל שחרורם של חמצן ושל פחמן דו-חמצני-מעידים על אנמיה. זו יכולה לנבוע מהפרעה המטולוגית, ממחסור בברזל ומדימומים.",ensure_ascii=False)
        patient.treatment=json.dumps(anemia,ensure_ascii=False)
        patient.treatment=json.dumps(hematologicalDisorder,ensure_ascii=False)
        patient.treatment=json.dumps(ironDef,ensure_ascii=False)
        patient.treatment=json.dumps(bleading,ensure_ascii=False)

    if((patient.gender == "woman" and age >17 and int(bloodtest.Hb)>16) or (patient.gender == "man" and age >17 and int(bloodtest.Hb)>18) or (age <=17 and int(bloodtest.Hb)>15.5)):
        patient.diagnose=json.dumps("ערכים גבוהים ברמת ההמוגלובין- המוגלובין הוא מרכיב בתוך הכדורית האדומה, אשר אחראי על קשירתם ועל שחרורם של חמצן ושל פחמן דו-חמצני.",ensure_ascii=False)

    #Crtn check
    if((age>=0 and age<=2 and int(bloodtest.Crtn)<0.2) or (age>=3 and age<=17 and int(bloodtest.Crtn)<0.5) or (age>=18 and age<=59 and int(bloodtest.Crtn)<0.6) or (age>=60 and int(bloodtest.Crtn)<0.6)):
        patient.diagnose=json.dumps("ערכים נמוכים בקריטאינין -  תוצר פירוק של מרכיב המיוצר בגוף ונמצא בשריר הקרוי קריאנין פוספט. בדיקת קריאטינין חשובה ביותר כיוון שהיא נותנת אמת מידה לגבי תפקוד הכליות. ערכים נמוכים נראים לרוב בחולים בעלי מסת שריר ירודה מאוד ואנשים בתת תזונה שאינם צורכים די חלבון",ensure_ascii=False)
        patient.treatment=json.dumps(muscleDisease,ensure_ascii=False)
        patient.treatment=json.dumps(malnutrition,ensure_ascii=False)
    if((age>=0 and age<=2 and int(bloodtest.Crtn)>0.5) or (age>=3 and age<=17 and int(bloodtest.Crtn)>1) or (age>=18 and age<=59 and int(bloodtest.Crtn)>1) or (age>=60 and int(bloodtest.Crtn)>1.2)):
        patient.diagnose=json.dumps("ערכים גבוהים בקריטאינין - תוצר פירוק של מרכיב המיוצר בגוף ונמצא בשריר הקרוי קריאנין פוספט. בדיקת קריאטינין חשובה ביותר כיוון שהיא נותנת אמת מידה לגבי תפקוד הכליות- הערכים עלולים להצביע על בעיה כלייתית ובמקרים חמורים על אי ספיקת כליות. ערכים גבוהים ניתן למצוא גם בעת שלשולים והקאות (הגורמים לפירוק מוגבר של שריר ולערכים גבוהים של קריאטינין), מחלות שריר וצריכה מוגברת של בשר.",ensure_ascii=False)
        patient.treatment=json.dumps(kidneyDisease,ensure_ascii=False)
        patient.treatment=json.dumps(muscleDisease,ensure_ascii=False)
        patient.treatment=json.dumps(meatInc,ensure_ascii=False)

    #Iron check
    if ((patient.gender == "man" and int(bloodtest.Iron)<60) or (patient.gender == "woman" and int(bloodtest.Iron)<48)):
        patient.diagnose=json.dumps("ערכים נמוכים בברזל - הברזל חיוני ליצירת ההמוגלובין - החלבון שנושא את החמצן בדם. נוסף על כך הוא משמש ליצירת אנזימים רבים אחרים. רמות נמוכות של ברזל מעידה בדרך כלל על תזונה לא מספקת או על עלייה בצורך בברזל (למשל בהריון) או על איבוד דם בעקבות דימום.",ensure_ascii=False)
        patient.treatment=json.dumps(diet,ensure_ascii=False)
        patient.treatment=json.dumps(bleading,ensure_ascii=False)
        #checkkkkkkkkkkkkk
    if ((patient.gender == "man" and int(bloodtest.Iron)>160) or (patient.gender == "woman" and int(bloodtest.Iron)>128)):
        patient.diagnose=json.dumps("ערכים גבוהים בברזל - הברזל חיוני ליצירת ההמוגלובין - החלבון שנושא את החמצן בדם. נוסף על כך הוא משמש ליצירת אנזימים רבים אחרים. רמות גבוהות של עלולים להצביע על הרעלת ברזל",ensure_ascii=False)
        patient.treatment=json.dumps(ironPoisoning,ensure_ascii=False)

    #HDL check
    if ((patient.ethiopian == False and (patient.gender == "man" and int(bloodtest.HDL)<29) or (patient.gender == "woman" and int(bloodtest.HDL)<34)) or (patient.ethiopian == True and (patient.gender == "man" and int(bloodtest.HDL)<34.8) or (patient.gender == "woman" and int(bloodtest.HDL)<40.8)) ):
        patient.diagnose=json.dumps("ערכים נמוכים באץ'-די-אל הקרוי גם הכולסטרול הטוב, הינו מולקולה דמוית חלבון, אשר נושאת את הכולסטרול מתאי הגוף אל הכבד,שם מפורק הכולסטרול. בכך מסייע ה-אץ'-די-אל לגוף להיפטר מעודפי שומנים. רמות נמוכותת עשויות להצביע על סיכון למחלות לב, על היפרליפידמיה (יתר שומנים בדם) או על סוכרת מבוגרים.",ensure_ascii=False)
        patient.treatment=json.dumps(heartDisease,ensure_ascii=False)
        patient.treatment=json.dumps(hiperlipidemia,ensure_ascii=False)
        patient.treatment=json.dumps(adultDiabetes,ensure_ascii=False)
    if ((patient.ethiopian == False and (patient.gender == "man" and int(bloodtest.HDL)>62) or (patient.gender == "woman" and int(bloodtest.HDL)>82)) or (patient.ethiopian == True and (patient.gender == "man" and int(bloodtest.HDL)>62*1.2) or (patient.gender == "woman" and int(bloodtest.HDL)>82*1.2)) ):
        patient.diagnose=json.dumps("ערכים גבוהים באץ'-די-אל הקרוי גם הכולסטרול הטוב, הינו מולקולה דמוית חלבון, אשר נושאת את הכולסטרול מתאי הגוף אל הכבד,שם מפורק הכולסטרול. בכך מסייע ה-אץ'-די-אל לגוף להיפטר מעודפי שומנים. רמות גבוהות לרוב אינן מזיקות. פעילות גופנית מעלה את רמות הכולסטרול הטוב.",ensure_ascii=False)

    #AP check
    if ((patient.eastCommunity == False and  int(bloodtest.AP)<30) or (patient.eastCommunity == True and  int(bloodtest.AP)<60)):
        patient.diagnose=json.dumps("ערכים נמוכים בפוספטזה אלקלית - התפקיד המטבולי של האנזים אינו ברור לגמרי. הוא קשור להעברת מרכיבים דרך ממברנות, וכן יש לו תפקיד בהסתיידות של העצם. האנזים נמצא ברקמות שונות בגוף, בעיקר בכבד, בדרכי המרה, במעי, בעצמות ובשליה. רמות נמוכות עשויות להצביע על תזונה לקויה שחסרים בה חלבונים. חוסר בוויטמינים כמו ויטמין בי12 , ויטמין סי, ויטמין בי6 וחומצה פולית. ",ensure_ascii=False)
        patient.treatment=json.dumps(diet,ensure_ascii=False)
        patient.treatment=json.dumps(vitaminDef,ensure_ascii=False)
    if ((patient.eastCommunity == False and  int(bloodtest.AP)>90) or (patient.eastCommunity == True and  int(bloodtest.AP)>120)):
        patient.diagnose=json.dumps("ערכים גבוהים  בפוספטזה אלקלית - התפקיד המטבולי של האנזים אינו ברור לגמרי. הוא קשור להעברת מרכיבים דרך ממברנות, וכן יש לו תפקיד בהסתיידות של העצם. האנזים נמצא ברקמות שונות בגוף, בעיקר בכבד, בדרכי המרה, במעי, בעצמות ובשליה. רמות גבוהות עלולים להצביע על מחלות כבד, מחלות בדרכי המרה, הריון, פעילות יתר של בלוטת התריס או שימוש בתרופות שונות",ensure_ascii=False)
        patient.treatment=json.dumps(liverDisease,ensure_ascii=False)
        patient.treatment=json.dumps(diseaseInBile,ensure_ascii=False)
        patient.treatment=json.dumps(overactiveThyroid,ensure_ascii=False)
        patient.treatment=json.dumps(variousMedications,ensure_ascii=False)
        if (patient.pregnancy == True):
            patient.treatment=json.dumps("המטופלת בהריון - נא לשים לב יכולות להיות רמות גבוהות בגלל ההריון",ensure_ascii=False)
        if (patient.pregnancy == False and patient.gender == "woman"):
            patient.treatment=json.dumps("עלול להיגרם בגלל הריון - הפנייה לשלילת הריון",ensure_ascii=False)

