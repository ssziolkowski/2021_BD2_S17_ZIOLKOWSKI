from .models import Vehicle
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

vehicles = [
    {
        'VIN': 'models.TextField(primary_key=True)1',
        'brand': 'models.TextField()1',
        'model': 'models.TextField()1',
        'version': 'models.TextField()1',
        'accessories': 'models.TextField()1',
        'plate_number': 'models.TextField()1',
        'current_mileage': 'models.IntegerField(default:0)1',
        'propose': 'models.TextField()1',
        'manager_id': 'models.ForeignKey1',
        'status': 'models.TextField(choices=STATUS)1',
        'path': 'f64b0864e862d3c122851be4770d6e9a_XL.jpg'
    },
    {
        'VIN': 'models.TextField(primary_key=True)2',
        'brand': 'models.TextField()2',
        'model': 'models.TextField()2',
        'version': 'models.TextField()2',
        'accessories': 'models.TextField()2',
        'plate_number': 'models.TextField()2',
        'current_mileage': 'models.IntegerField(default:0)2',
        'propose': 'models.TextField()2',
        'manager_id': 'models.ForeignKey2',
        'status': 'models.TextField(choices=STATUS)2',
        'path': '1d96f93186b635279bd7d3054bcfa104_800x600.jpg'
    },
    {
        'VIN': 'models.TextField(primary_key=True)3',
        'brand': 'models.TextField()3',
        'model': 'models.TextField()3',
        'version': 'models.TextField()3',
        'accessories': 'models.TextField()3',
        'plate_number': 'models.TextField()3',
        'current_mileage': 'models.IntegerField(default:0)3',
        'propose': 'models.TextField()3',
        'manager_id': 'models.ForeignKey3',
        'status': 'models.TextField(choices=STATUS)3',
        'path': 'pobrane.jpg'
    },
    {
        'VIN': 'models.TextField(primary_key=True)4',
        'brand': 'models.TextField()4',
        'model': 'models.TextField()4',
        'version': 'models.TextField()4',
        'accessories': 'models.TextField()4',
        'plate_number': 'models.TextField()4',
        'current_mileage': 'models.IntegerField(default:0)4',
        'propose': 'models.TextField()4',
        'manager_id': 'models.ForeignKey4',
        'status': 'models.TextField(choices=STATUS)4',
        'path': '61169147-dedilovo-russia-aug-6-2016-old-soviet-tractor-t-74-one-of-the-most-mass-soviet-tractors-produced-in-.jpg'
    },
    {
        'VIN': 'models.TextField(primary_key=True)5',
        'brand': 'models.TextField()5',
        'model': 'models.TextField()5',
        'version': 'models.TextField()5',
        'accessories': 'models.TextField()5',
        'plate_number': 'models.TextField()5',
        'current_mileage': 'models.IntegerField(default:0)5',
        'propose': 'models.TextField()5',
        'manager_id': 'models.ForeignKey5',
        'status': 'models.TextField(choices=STATUS)5',
        'path': 'pobrane (1).jpg'
    }
]


def fleetManager(request):
    context = {
        'vehicles': Vehicle.objects.all()
    }
    return render(request, 'manager/fleetManager.html', context)


def allVehicles(request):
    context = {
        'vehicles': vehicles
    }
    return render(request, 'manager/allVehicles.html', context)


def login(request):
    return render(request, 'manager/login.html')


@csrf_exempt 
def addVehicle(request):
    if request.method == "POST":
            form = VehiclesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                post = form.save(commit=False)
                post.save()
                return redirect('fleetManager')
            else:
                form = VehiclesForm()
       
    return render(request, 'manager/addVehicle.html')
    

def rentVehicle(request):
    return render(request, 'manager/rentVehicle.html')


def selectedVehicle(request):
    return render(request, 'manager/selectedVehicle.html')


def adminpanel(request):
    return render(request, 'manager/adminpanel.html')


def addperson(request):
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


