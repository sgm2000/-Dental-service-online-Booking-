from contextlib import redirect_stdout
import email
from math import ceil
from sqlite3 import Time
import this
from django.shortcuts import render,redirect
from django.views import generic
from application.settings import LOGIN_REDIRECT_URL
from booking.forms import BookingForm, UserForm
from booking.models import Appointment, Service,User, STime
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.

def homepage(request):
    services = Service.objects.all()
    n = len(services)
    nSlides = n//4 + ceil((n/4))
    params = {'n0_of_slides':nSlides,'range':range(1,nSlides),'service':services}
    return render(request,'homepage.html',params)


def userhome(request):
    uname = request.COOKIES.get('uname')
    u = User.objects.get(username = uname)
    services = Service.objects.all()
    n = len(services)
    nSlides = n//4 + ceil((n/4))
    params = {'n0_of_slides':nSlides,'range':range(1,nSlides),'service':services}
    return render(request,'userhome.html',params)

def about(request):
    return render(request,'about.html')

class serviceListView(generic.ListView):
    model = Service
    template_name = 'service_list.html'

class service2ListView(generic.ListView):
    model = Service
    template_name = 'service_list2.html'

class serviceDetailView(generic.DetailView):
    model = Service
    template_name = 'service_detail.html'

def register(request):
     submitted = False
     if request.method == 'POST':
         form = UserForm(request.POST)
         if form.is_valid():
             form.save()
             return HttpResponseRedirect('/register/?submitted=True')
     else:
         form = UserForm()
         if 'submitted' in request.GET:
             submitted = True
     return render(request, 'register.html', {'form': form, 'submitted': submitted})

def userlogin(request):
      if request.method == 'POST':
          uname=request.POST.get('uname')
          pwd=request.POST.get('pwd')
          if 'next' in request.POST:
              return redirect(request.POST.get('next'))
          else:
            u=User.objects.filter(username=uname,password=pwd)
            if(u):
                services = Service.objects.all()
                n = len(services)
                nSlides = n//4 + ceil((n/4))
                params = {'n0_of_slides':nSlides,'range':range(1,nSlides),'service':services}
                response= render(request,'userhome.html',params)
                response.set_cookie('uname',uname)
                return response
            else:
                return render(request,'userlogin.html')

      else:
         return render(request,'userlogin.html')

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def booking(request):
     submitted = False
     if request.method == 'POST':
         service=request.POST.get('service')
         date=request.POST.get('date')
         timing=request.POST.get('timings')
         uname=request.COOKIES.get('uname')
         u=User.objects.get(username=uname)
         uid=u.id
         name = u.first_name
         email = u.email
         obj = STime.objects.get(pk = timing)
         sobj = Service.objects.get(pk = service)
         form = Appointment(service_id=service,name=name,email=email,date=date,timings=obj,user_id=uid)
         form.save()

         template = render_to_string('email_body.html',{'name':name,'service':sobj,'date':date,'time':obj})
         email_sending = EmailMessage(
             'Thank You',
             template,
             settings.EMAIL_HOST_USER,
             [email],
         )
         email_sending.fail_silently = False
         email_sending.send()

         return HttpResponseRedirect('/book/?submitted=True')
     else:
         form = BookingForm()
         if 'submitted' in request.GET:
             submitted = True
     return render(request, 'appointment.html', {'form': form, 'submitted': submitted})

class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = 'appointment_list.html'

def logout(request):
    services = Service.objects.all()
    n = len(services)
    nSlides = n//4 + ceil((n/4))
    params = {'n0_of_slides':nSlides,'range':range(1,nSlides),'service':services}
    return render(request,'homepage.html',params)