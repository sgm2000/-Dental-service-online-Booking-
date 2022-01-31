from distutils.command.upload import upload
from pickle import TRUE
from pyexpat import model
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    email=models.EmailField()
    phoneno=models.CharField(max_length=10)
    address = models.CharField(max_length=300,default="")


class Service(models.Model):
    service_id = models.AutoField
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to = 'serv/images')
    def __str__(self):
        return self.title

class STime(models.Model):
    STime_id = models.AutoField
    timings = models.CharField(max_length=30)
    def __str__(self):
        return self.timings

class Appointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    date = models.DateField()
    timings = models.ForeignKey(STime,on_delete=models.CASCADE)


