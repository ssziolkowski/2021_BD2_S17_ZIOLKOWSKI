from .models import Company, Vehicle
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def fleetManager(request):
    context = {
        'vehicles': Vehicle.objects.all()
    }
    return render(request, 'manager/fleetManager.html', context)


def allVehicles(request):
    context = {
        'vehicles': Vehicle.objects.all()
    }
    return render(request, 'manager/allVehicles.html', context)

def filterVehicle_view(request, otype): 
    vehicle = Vehicle.objects.filter(category=otype)
    context={
      'vehicles':vehicle
    }
    return render(request, 'manager/allVehicles.html', context)


def login(request):
    return render(request, 'manager/login.html')


def addVehicle(request):
    if request.method == "POST":
            form = VehiclesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                post = form.save(commit=False)
                #print(post.picture)
                post.save()
                return redirect('fleetManager')
            else:
                form = VehiclesForm()
       
    return render(request, 'manager/addVehicle.html')
    
def selectedVehicle_view(request, ovin): 
    vehicle = Vehicle.objects.filter(VIN=ovin).first()
    context={
      'vehicle':vehicle
    }
    return render(request, "manager/selectedVehicle.html", context)


def rentVehicle(request):
    return render(request, 'manager/rentVehicle.html')


def selectedVehicle(request):
    return render(request, 'manager/selectedVehicle.html')


def adminpanel(request):
    return render(request, 'manager/adminpanel.html')


def addperson(request):
    if request.method == "POST":
            form = PersonForm(request.POST)
            if form.is_valid():
                form.save()
                person = form.save(commit=False)
                person.companyID=Company.objects.get(id=1)
                person.save()
                return redirect('fleetManager')
            else:
                form = PersonForm()
    return render(request, 'manager/addperson.html')


def addservice(request):
    return render(request, 'manager/addservice.html')


def addserviceplan(request):
    return render(request, 'manager/addserviceplan.html')


def editperson(request):
    return render(request, 'manager/editperson.html')


def editvehicle(request):
    return render(request, 'manager/editVehicle.html')


def editservice(request):
    return render(request, 'manager/editservice.html')


def editserviceplan(request):
    return render(request, 'manager/editserviceplan.html')


