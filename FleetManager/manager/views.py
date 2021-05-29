from django.http.response import HttpResponseRedirect
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import *
from django.utils import timezone


def fleetManager(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

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
    if id == -1:
        return redirect('login')

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
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    vehicle = Vehicle.objects.filter(category=otype)
    context = {
        'vehicles': vehicle,
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', ''),
        'company': request.session.get('company', -1)
    }
    return render(request, 'manager/allVehicles.html', context)


def person_update_view(request, upid):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    obj = Person.objects.filter(ID=upid).first()
    form = PersonForm(request.POST or None, instance=obj)
    context = {
        'person': obj,
        'persons': Person.objects.all().order_by("ID"),
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', ''),
        'company': request.session.get('company', -1)
    }
    if form.is_valid():
        form.save()
        return render(request, "manager/editPersonel.html", context)
    return render(request, "manager/editPerson.html", context)


def login(request):
    request.session['id'] = -1
    request.session['user'] = 'none'
    request.session['name'] = ''
    request.session['company'] = -1

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = Person.objects.filter(
                login=data['login'], password=data['password']).first()
            if user is None:
                company = Company.objects.filter(
                    login=data['login'], password=data['password']).first()
                if company is None:
                    request.session['id'] = -1
                    request.session['user'] = 'none'
                    request.session['name'] = ''
                    request.session['company'] = -1
                    return redirect('login')
                else:
                    request.session['id'] = company.id
                    request.session['user'] = 'admin'
                    request.session['name'] = company.name
                    request.session['company'] = -1
                    return redirect('adminPanel')
            else:
                request.session['id'] = user.ID
                if Manager.objects.filter(personal_ID=user.ID).first() is not None:
                    request.session['user'] = 'manager'
                else:
                    request.session['user'] = 'person'
                request.session['name'] = user.name + ' ' + user.surname
                request.session['company'] = user.companyID.id
                return redirect('fleetManager')
        else:
            form = VehiclesForm()
    else:
        return render(request, 'manager/login.html')


def addVehicle(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    if request.method == "POST":
        form = VehiclesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            post = form.save(commit=False)
            post.save()
            return redirect('fleetManager')
        else:
            form = VehiclesForm()

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/addVehicle.html', context)


def selectedVehicle_view(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    if request.method == "POST":
        form = VehiclesForm(request.POST)
        vin = request.POST.get("VIN", "NOVIN")

    vehicle = Vehicle.objects.filter(VIN=vin).first()
    id = request.session.get('id', -1)
    context = {
        'vehicle': vehicle,
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', '')
    }

    return render(request, "manager/selectedVehicle.html", context)


def rentVehicle(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/rentVehicle.html', context)


def selectedVehicle(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/selectedVehicle.html', context)


def adminPanel(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/adminPanel.html', context)


def addPerson(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

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

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addPerson.html', context)


def addService(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            service = form.save(commit=False)
            service.save()
            return redirect('addService')
        else:
            form = ServiceForm()

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addService.html', context)


def addServiceplan(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    if request.method == "POST":
        form = ServiceplanForm(request.POST)
        if form.is_valid():
            form.save()
            serviceplan = form.save(commit=False)
            serviceplan.save()
            return redirect('addServiceplan')
        else:
            form = ServiceplanForm()

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addServiceplan.html', context)


def editPerson(request, pid):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    obj = get_object_or_404(Person, ID=pid)
    person = obj
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
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editPersonel.html', context)


def editPersonel(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'persons': Person.objects.all().order_by("ID")
    }
    return render(request, 'manager/editPersonel.html', context)


def editVehicle(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editVehicle.html', context)


def editService(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editService.html', context)


def editServiceplan(request):
    id = request.session.get('id', -1)
    if id == -1:
        return redirect('login')

    context = {
        'id': id,
        'user': request.session.get('user', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editServiceplan.html', context)
