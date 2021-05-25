from django.http.response import HttpResponseRedirect
from .models import Company, Vehicle
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import *
from django.utils import timezone

def fleetManager(request):
    context = {
        'vehicles': Vehicle.objects.all()
    }
    return render(request, 'manager/fleetManager.html', context)


def allVehicles(request):
    search=request.GET.get("search",None)
    if search is None:
        context = {
            'vehicles': Vehicle.objects.all()
        }
    else:
        context = {
            'vehicles': Vehicle.objects.filter(model__icontains=search)
        }
    return render(request, 'manager/allVehicles.html', context)


def filterVehicle_view(request, otype): 
    vehicle = Vehicle.objects.filter(category=otype)
    context={
      'vehicles':vehicle
    }
    return render(request, 'manager/allVehicles.html', context)


def person_detail_view(request, id):
    context = {}
    context["person_data"] = Person.objects.get(id = id)
    return render(request, "editPerson.html", context)


def person_update_view(request, id):
    context ={}
    obj = get_object_or_404(Person, ID = id)
    form = PersonForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+id)
    context["form"] = form
 
    return render(request, "editPerson.html", context)


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


def adminPanel(request):
    return render(request, 'manager/adminPanel.html')


def addPerson(request):
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
    return render(request, 'manager/addPerson.html')


def addService(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            service = form.save(commit=False)
            service.save()
            return redirect('addService')
        else:
            form = ServiceForm()
    return render(request, 'manager/addService.html')
 

def addServiceplan(request):
    if request.method == "POST":
        form = ServiceplanForm(request.POST)
        if form.is_valid():
            form.save()
            serviceplan = form.save(commit=False)
            serviceplan.save()
            return redirect('addServiceplan')
        else:
            form = ServiceplanForm()
    return render(request, 'manager/addServiceplan.html')


def editPerson(request, pid):
    obj = get_object_or_404(Person, ID = pid)
    person = obj
    context={
      'person':person
    }
    form = PersonForm(request.POST, instance = obj)
    if form.is_valid():
        form.save()
        return render(request, 'manager/editPersonel.html')

    return render(request, 'manager/editPerson.html', context)


def editPersonel(request):
    context = {
        'persons': Person.objects.all()
    }
    return render(request, 'manager/editPersonel.html', context)


def editVehicle(request):
    return render(request, 'manager/editVehicle.html')


def editService(request):
    return render(request, 'manager/editService.html')


def editServiceplan(request):
    return render(request, 'manager/editServiceplan.html')


