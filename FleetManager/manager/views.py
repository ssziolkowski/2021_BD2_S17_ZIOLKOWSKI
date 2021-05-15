from django.shortcuts import render
from django.http import HttpResponse


vehicles = [
    {
        'a1': 'dupa',
        'a2': 'tralala'
    },
    {
        'a1': 'dupa2',
        'a2': 'tralala2'
    }
]


def fleetManager(request):
    context = {
        'vehicles': vehicles
    }
    return render(request, 'manager/fleetManager.html', context)


def allVehicles(request):
    return render(request, 'manager/allVehicles.html')


def login(request):
    return render(request, 'manager/login.html')


def addVehicle(request):
    return render(request, 'manager/addVehicle.html')


def rentVehicle(request):
    return render(request, 'manager/rentVehicle.html')


def selectedVehicle(request):
    return render(request, 'manager/selectedVehicle.html')
