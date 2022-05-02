from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=8, null = True, default = None)
    user_id = models.CharField(max_length=9,null = True)
    password = models.CharField(max_length=10, null=True, default = None)

    def __str__(self):
        return f'Name: {self.name}, ID: {self.user_id}, Password: {self.password}'


class BloodTest(models.Model):    
    WBC = models.CharField(max_length=10, null = True, default = None)
    Neut = models.CharField(max_length=10,null = True, default = None)
    Lymph = models.CharField(max_length=10,null = True, default = None)    
    RBC = models.CharField(max_length=10,null = True, default = None)
    HCT = models.CharField(max_length=10,null = True, default = None)
    Urea = models.CharField(max_length=10, null = True, default = None)
    Hb = models.CharField(max_length=10, null = True, default = None) 
    Crtn = models.CharField(max_length=10, null = True, default = None)        
    Iron = models.CharField(max_length=10,null = True, default = None)
    HDL = models.CharField(max_length=10,null = True, default = None)
    AP = models.CharField(max_length=10, null = True, default = None)


class Patient(models.Model):
    name = models.CharField(max_length=8, null = True, default = None)
    lastName = models.CharField(max_length=8, null = True, default = None)
    patient_id = models.CharField(max_length=9,null = True,default = None)
    age = models.CharField(max_length=9,null = True,default = None)
    gender = models.CharField(max_length=9,null = True,default = None)
    smoke = models.BooleanField(null= True,default = False)
    eastCommunity = models.BooleanField(null= True,default = False)
    pregnancy = models.BooleanField(null= True,default = False)
    ethiopian =  models.BooleanField(null= True,default = False)
    medicine = models.BooleanField(null= True,default = False) #before the meeting
    bloodTest = models.ForeignKey(BloodTest, on_delete = models.CASCADE,null= True,default = None)
    diagnose = models.CharField(max_length=300,null = True,default = None)
    treatment = models.CharField(max_length=500,null = True,default = None)


    def __str__(self):
        return f'Name: {self.name}, ID: {self.patient_id}, Smoke: {self.smoke}'
