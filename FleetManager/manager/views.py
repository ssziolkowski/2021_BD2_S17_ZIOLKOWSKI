from django.http.response import HttpResponseRedirect
from .models import Company, Vehicle
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import *
from django.utils import timezone


def fleetManager(request):
    id = request.session.get('id', -1)
    context = {
        'vehicles': Vehicle.objects.all(),
        'id': id,
        'user': request.session.get('user', 'none')
    }
    user = Person.objects.filter(ID=id).first()
    if user is not None:
        context['name'] = user.name + ' ' + user.surname
        context['company'] = user.companyID
    else:
        context['name'] = 'FleetManager'

    return render(request, 'manager/fleetManager.html', context)


def allVehicles(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none')
    }
    user = Person.objects.filter(ID=id).first()
    if user is not None:
        context['name'] = user.name + ' ' + user.surname
        context['company'] = user.companyID
    else:
        context['name'] = 'FleetManager'

    search = request.GET.get("search", None)
    if search is None:
        context['vehicles'] = Vehicle.objects.all()
    else:
        context['vehicles'] = Vehicle.objects.filter(model__icontains=search)

    return render(request, 'manager/allVehicles.html', context)


def filterVehicle_view(request, otype):
    vehicle = Vehicle.objects.filter(category=otype)
    context = {
        'vehicles': vehicle
    }
    return render(request, 'manager/allVehicles.html', context)


def person_update_view(request, upid):
    context = {}
    obj = Person.objects.filter(ID=upid).first()
    form = PersonForm(request.POST or None, instance=obj)
    context = {
        'person': obj,
        'persons': Person.objects.all().order_by("ID")
    }
    if form.is_valid():
        form.save()
        return render(request, "manager/editPersonel.html", context)
    return render(request, "manager/editPerson.html", context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            userFilter = Person.objects.filter(
                login=data['login'], password=data['password'])
            user = userFilter.first()
            if user is None:
                request.session['id'] = -1
                request.session['user'] = 'none'
                request.session['name'] = 'FleetManager'
                return redirect('login')
            else:
                request.session['id'] = user.ID
                request.session['user'] = 'person'
                request.session['name'] = user.name + ' ' + user.surname
                return redirect('fleetManager')
        else:
            form = VehiclesForm()

    context = {
        'id': -1,
        'user': 'none',
        'name': 'FleetManager'
    }
    return render(request, 'manager/login.html', context)


def logout(request):
    request.session['id'] = -1
    request.session['user'] = 'none'
    request.session['name'] = 'FleetManager'

    return redirect('login')


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

    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/addVehicle.html', context)


def selectedVehicle_view(request, ovin):
    vehicle = Vehicle.objects.filter(VIN=ovin).first()
    id = request.session.get('id', -1)
    context = {
        'vehicle': vehicle,
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, "manager/selectedVehicle.html", context)


def rentVehicle(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/rentVehicle.html', context)


def selectedVehicle(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/selectedVehicle.html', context)


def adminPanel(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/adminPanel.html', context)


def addPerson(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            person = form.save(commit=False)
            person.companyID = Company.objects.get(id=1)
            person.save()
            return redirect('addPerson')
        else:
            form = PersonForm()

    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addPerson.html', context)


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

    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addService.html', context)


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

    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addServiceplan.html', context)


def editPerson(request, pid):
    obj = get_object_or_404(Person, ID=pid)
    person = obj
    id = request.session.get('id', -1)
    context = {
        'person': person,
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    if request.method == "POST":
        return render(request, 'manager/editPerson.html', context)

    return render(request, 'manager/editPersonel.html', context)


def updatePerson(request, pid):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editPersonel.html', context)


def editPersonel(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'persons': Person.objects.all().order_by("ID")
    }
    return render(request, 'manager/editPersonel.html', context)


def editVehicle(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editVehicle.html', context)


def editService(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editService.html', context)


def editServiceplan(request):
    id = request.session.get('id', -1)
    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editServiceplan.html', context)
