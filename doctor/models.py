from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=8, null = True, default = None)
    user_id = models.CharField(max_length=9,null = True)
    password = models.CharField(max_length=10, null=True, default = None)

    def __str__(self):
        return f'Name: {self.name}, ID: {self.user_id}, Password: {self.password}'

