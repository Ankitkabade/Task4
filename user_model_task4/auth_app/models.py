from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    GENDER = [
        ('male','male'),
        ('female','female'),
        ('other','other')
    ]
    ROLE=[
        ('manager','manager'),
        ('team_leader','team_leader'),
        ('developer','developer')

    ]
    gender = models.CharField(max_length=6,choices =GENDER,default="male")
    address = models.TextField(blank=True,null=True)
    pincode = models.CharField(max_length=6,blank=True,null=True)
    city = models.CharField(max_length=40,blank=True,null=True)
    role = models.CharField(max_length=20,default="manager",choices=ROLE)
    company=models.CharField(max_length=50,blank=True,null=True)
    contact =PhoneNumberField(region="IN",blank=True,null=True)


