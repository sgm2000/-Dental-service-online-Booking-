from time import time
from django.contrib import admin
from booking.models import Service, STime
# Register your models here.


admin.site.register(Service)
admin.site.register(STime)