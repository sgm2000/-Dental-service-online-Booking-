from pyexpat import model
from socket import fromshare
from tkinter import Widget
from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
from booking.models import Appointment, User
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(ModelForm):
      required_css_class = 'required'
      password=forms.CharField(widget=forms.PasswordInput)
      class Meta:
          model = User
          fields = '__all__'

class BookingForm(ModelForm):
    required_css_class = 'required'
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
    
    class Meta:
        model = Appointment
        fields = ('service','date','timings')
        widgets = {'date' : DateInput()}
        