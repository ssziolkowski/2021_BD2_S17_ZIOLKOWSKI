import io
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http.response import FileResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import *
from django.utils import timezone
from django.db.models import Q
import pdfkit
import datetime
from reportlab.pdfgen import canvas
import re
import zipfile

def managerPanel(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    id = request.session.get('id', -1)
    context = {
        'vehicles': Manager.objects.select_related('personal_ID').filter(personal_ID=id),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', ''),
    }
    return render(request, 'manager/managerPanel.html', context)


def managerManager(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', ''),
        'managers': Manager.objects.annotate(num_cars=Count('personal_ID_id')).order_by('id'),
        #'mmanagers': Manager.objects.aggregate(num_cars=Count('personal_ID')),

        'records': Manager.objects.select_related('personal_ID')

        # 'persons': Person.objects.filter(companyID=request.session.get('company', -1)).select_related() .order_by("ID"),
    }
    return render(request, 'manager/managerManager.html', context)


def fleetManager(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')
    if request.session.get('currentUser', 'none') == 'admin':
        return redirect('adminPanel')
    if request.session.get('currentUser', 'none') == 'manager':
        return redirect('managerPanel')

    context = {
        'vehicles': Vehicle.objects.filter(companyID=request.session.get('company', -1)),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }
    return render(request, 'manager/fleetManager.html', context)


def allVehicles(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }

    search = request.GET.get("search", None)
    if search is None:
        context['vehicles'] = Vehicle.objects.filter(
            companyID=request.session.get('company', -1))
    else:
        context['vehicles'] = Vehicle.objects.filter(
            Q(model__icontains=search) | Q(brand__icontains=search),
            companyID=request.session.get('company', -1))

    return render(request, 'manager/allVehicles.html', context)


def filterVehicle_view(request, otype):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'vehicles': Vehicle.objects.filter(category=otype, companyID=request.session.get('company', -1)),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }
    return render(request, 'manager/allVehicles.html', context)


def person_update_view(request, upid):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    person = Person.objects.filter(ID=upid).first()
    form = PersonForm(request.POST or None, instance=person)
    context = {
        'person': person,
        'persons': Person.objects.filter(companyID=request.session.get('company', -1)).order_by("ID"),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }

    if form.is_valid():
        post = form.save(commit=False)
        saveChangeLog(id=request.session.get('company', -1),
                post=post, name="changed", obj2 = post, obj = Person.objects.filter(ID=post.ID).first())
        post.save()
        return render(request, "manager/editPersonel.html", context)
    return render(request, "manager/editPerson.html", context)


def manager_update_view(request, umid):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    manager = Manager.objects.filter(personal_ID_id=umid).annotate(num_cars=Count('VIN')).first()
    vehicles = Manager.objects.filter(personal_ID_id=umid).select_related('VIN')
    #form = ManagerForm(request.POST or None, instance=manager)
    context = {
        'manager': manager,
        #    'persons': Person.objects.filter(companyID=request.session.get('company', -1)).order_by("ID"),
        'user': request.session.get('currentUser', 'none'),
        'vehicles': vehicles,
        'name': request.session.get('name', '')
    }

    # if form.is_valid():
    #    post = form.save()
    #    saveLog(id=request.session.get('company', -1),
    #            post=post, name="changed")
    #    return render(request, "manager/manager.html", context)
    return render(request, "manager/manager.html", context)

def add_manager_vehicle_view(request, mid):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    managed_vehicles = Manager.objects.select_related('VIN')
    manager = Manager.objects.filter(personal_ID_id=mid).first()
    vehicles = Vehicle.objects.filter(companyID=request.session.get('company', -1)).exclude(
            VIN__in=[o.VIN_id for o in managed_vehicles])
    #form = ManagerForm(request.POST or None, instance=manager)
    context = {
        'manager': manager,
        #    'persons': Person.objects.filter(companyID=request.session.get('company', -1)).order_by("ID"),
        'user': request.session.get('currentUser', 'none'),
        'vehicles': vehicles,
        'name': request.session.get('name', '')
    }

    # if form.is_valid():
    #    post = form.save()
    #    saveLog(id=request.session.get('company', -1),
    #            post=post, name="changed")
    #    return render(request, "manager/manager.html", context)
    return render(request, "manager/addManagerVehicle.html", context)


def addManagerVehicle(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = ManagerForm(request.POST)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.save()
            saveLog(id=request.session.get('company', -1),
                    post=manager, name="added")
            return redirect('managerManager')
        else:
            form = ManagerForm()
        print(form.is_valid)
        print(form.errors)
    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return redirect('managerManager')


def login(request):
    request.session['id'] = -1
    request.session['currentUser'] = 'none'
    request.session['name'] = ''
    request.session['company'] = -1

    context = {
        'id': -1,
        'user': 'none',
        'name': '',
        'company': -1
    }

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
                    request.session['currentUser'] = 'none'
                    request.session['name'] = ''
                    request.session['company'] = -1
                    return redirect('login')
                else:
                    request.session['id'] = company.id
                    request.session['currentUser'] = 'admin'
                    request.session['name'] = company.name
                    request.session['company'] = company.id
                    return redirect('adminPanel')
            else:
                request.session['id'] = user.ID
                if Manager.objects.filter(personal_ID=user.ID).first() is not None:
                    request.session['currentUser'] = 'manager'
                    request.session['name'] = user.name + ' ' + user.surname
                    request.session['company'] = user.companyID.id
                    return redirect('managerPanel')
                else:
                    request.session['currentUser'] = 'person'
                    request.session['name'] = user.name + ' ' + user.surname
                    request.session['company'] = user.companyID.id
                    return redirect('fleetManager')
        else:
            form = VehiclesForm()
    else:
        return render(request, 'manager/login.html', context)


def addVehicle(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = VehiclesForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.companyID = Company.objects.get(
                id=request.session.get('company', -1))
            post.save()
            saveLog(id=request.session.get(
                'company', -1), post=post, name="added")
            return redirect('allVehicles')
        else:
            form = VehiclesForm()

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/addVehicle.html', context)


def selectedVehicle_view(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = VehiclesForm(request.POST)
        vin = request.POST.get("VIN", "NOVIN")

    vehicle = Vehicle.objects.filter(VIN=vin).first()
    context = {
        'vehicle': vehicle,
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }

    return render(request, "manager/selectedVehicle.html", context)


def managedVehicle(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    if request.method == "POST":
        vin = request.POST.get("vehicle_id", "NOVIN")
        id = request.POST.get("id", -1)
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            service = form.save(commit=False)
            service.companyID = Company.objects.get(
                id=request.session.get('company', -1))
            service.plan = Serviceplan.objects.filter(
                id=id).first()
            service.save()

        vehicle = Vehicle.objects.filter(VIN=vin).first()
        context['vehicle'] = vehicle

        services = Service.objects.exclude(
            plan=None).filter(vehicle_id=vehicle)
        serviceplan = Serviceplan.objects.exclude(
            id__in=[o.plan.id for o in services]).filter(
                brand=vehicle.brand, model=vehicle.model, version=vehicle.version, accessories=vehicle.accessories)
           
        context['serviceplan'] = serviceplan

    return render(request, 'manager/managedVehicle.html', context)

# Renting Vehicle


def rentVehicle(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = VehiclesForm(request.POST)
        vin = request.POST.get("VIN", "NOVIN")

    vehicle = Vehicle.objects.filter(VIN=vin).first()

    context = {
        'vehicle': vehicle,
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/rentVehicle.html', context)


def reserveVehicle(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = ReserveForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.renter_id = Person.objects.filter(
                ID=request.session.get('id', -1)).first()
            case_1 = Rental.objects.filter(
                vehicle_id=rental.vehicle_id, rent_start__lte=rental.rent_start, rent_end__gte=rental.rent_start).exists()
            case_2 = Rental.objects.filter(
                vehicle_id=rental.vehicle_id, rent_start__lte=rental.rent_end, rent_end__gte=rental.rent_end).exists()
            case_3 = Rental.objects.filter(
                vehicle_id=rental.vehicle_id, rent_start__gte=rental.rent_start, rent_end__lte=rental.rent_end).exists()

            if case_1 or case_2 or case_3 or (rental.rent_start > rental.rent_end):

                context = {
                    'vehicle': Vehicle.objects.filter(VIN=rental.vehicle_id.VIN).first(),
                    'user': request.session.get('currentUser', 'none'),
                    'name': request.session.get('name', 'FleetManager'),
                    'error': "This vehicle is not available on your selected dates"
                }
                return render(request, 'manager/rentVehicle.html', context)

            rental.rent_status = 'reserved'
            rental.save()
            rentalLog(name='reserved', person=rental.renter_id,
                      companyId=request.session.get('company', -1), post=rental)

            if rental.rent_start == datetime.date.today():
                context = {
                    'vehicle': Vehicle.objects.filter(VIN=rental.vehicle_id.VIN).first(),
                    'user': request.session.get('currentUser', 'none'),
                    'name': request.session.get('name', 'FleetManager'),
                    'error': "This vehicle is not available on your selected dates"
                }
                return render(request, 'manager/startRent.html', context)

            else:
                return redirect('fleetManager')
        else:
            form = ReserveForm()

    context = {
        'vehicles': Vehicle.objects.filter(
            companyID=request.session.get('company', -1)),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return(request, 'fleetManager', context)


def startRent(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        starting_mileage = request.POST.get("starting_mileage", -1)
        vin = request.POST.get("VIN", "NOVIN")

    vehicle = Vehicle.objects.filter(VIN=vin).first()

    rental = Rental.objects.filter(
        vehicle_id=vehicle, rent_start=datetime.date.today()).first()

    if rental is not None:
        rental.starting_mileage = starting_mileage
        rental.rent_status = 'rented'
        rentalLog(name='rented', person=rental.renter_id,
                  companyId=request.session.get('company', -1), post=rental)
        rental.save()

    context = {
        'vehicles': Vehicle.objects.filter(companyID=request.session.get('company', -1)),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/fleetManager.html', context)


def endRent(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        final_mileage = request.POST.get("final_mileage", -1)
        cost = request.POST.get("cost", 0)
        vin = request.POST.get("VIN", "NOVIN")
        description = request.POST.get("description", "NO description")

    vehicle = Vehicle.objects.filter(VIN=vin).first()

    rental = Rental.objects.filter(
        vehicle_id=vehicle, rent_end=datetime.date.today()).first()

    if rental is not None:
        rental.final_mileage = final_mileage
        rental.exploitation_cost = cost
        rental.costs_description = description
        rental.rent_status = 'given'
        rentalLog(name='returned', person=rental.renter_id,
                  companyId=request.session.get('company', -1), post=rental)
        rental.save()

    context = {
        'vehicles': Vehicle.objects.filter(companyID=request.session.get('company', -1)),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/fleetManager.html', context)


#
#
# Your Vehicles

def yourVehiclesView(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    rental = Rental.objects.filter(renter_id=request.session.get('id', -1))

    rentalList = []

    for rent in rental:
        tempList = []
        tempList.append(rent.vehicle_id.model)
        tempList.append(rent.vehicle_id.picture.url)
        tempList.append(rent.vehicle_id.VIN)
        tempList.append(rent.rent_id)
        tempList.append(rent.rent_start)
        tempList.append(rent.rent_end)
        tempList.append(rent.rent_status)
        rentalList.append(tempList)

    context = {
        'rental': rentalList,
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/yourVehicles.html', context)


def rentalDetailsView(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'vehicle': Vehicle.objects.filter(VIN=request.POST.get("VIN", "NOVIN")).first(),
        'rental': Rental.objects.filter(rent_id=request.POST.get("rentID", -1)).first(),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'error': "This vehicle is not available on your selected dates"
    }
    return render(request, 'manager/rentalDetails.html', context)


def toStartRent(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'vehicle': Vehicle.objects.filter(VIN=request.POST.get("VIN", "NOVIN")).first(),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'error': "This vehicle is not available on your selected dates"
    }
    return render(request, 'manager/startRent.html', context)


####
###
####

def toEndRent(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'vehicle': Vehicle.objects.filter(VIN=request.POST.get("VIN", "NOVIN")).first(),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'error': "This vehicle is not available on your selected dates"
    }
    return render(request, 'manager/endRent.html', context)


def selectedVehicle(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/selectedVehicle.html', context)


def adminPanel(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/adminPanel.html', context)


def addPerson(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.companyID = Company.objects.get(
                id=request.session.get('company', -1))
            person.save()
            saveLog(id=request.session.get('company', -1),
                    post=person, name="added")
            return redirect('addPerson')
        else:
            form = PersonForm()

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addPerson.html', context)


def addService(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            saveLog(id=request.session.get('company', -1),
                    post=service, name="added")
            return redirect('addService')
        else:
            form = ServiceForm()

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addService.html', context)


def addServiceplan(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    if request.method == "POST":
        form = ServiceplanForm(request.POST)
        if form.is_valid():
            serviceplan = form.save(commit=False)
            serviceplan.status = False
            serviceplan.save()
            saveLog(id=request.session.get('company', -1),
                    post=serviceplan, name="added")
            return redirect('addServiceplan')

        else:
            form = ServiceplanForm()
    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/addServiceplan.html', context)


def editPerson(request, pid):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    obj = get_object_or_404(Person, ID=pid)
    person = obj
    context = {
        'person': person,
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    if request.method == "POST":
        return render(request, 'manager/editPerson.html', context)

    return render(request, 'manager/editPersonel.html', context)


def editPersonel(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')
    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'persons': Person.objects.filter(companyID=request.session.get('company', -1)).order_by("ID")
    }
    search = request.GET.get("phrase", None)
    if search is None:
        context['persons'] = Person.objects.filter(
            companyID=request.session.get('company', -1))
    else:
        filter = request.GET.get("filter", None)
        filterPhrase = filter + '__icontains'
        context['persons'] = Person.objects.filter(**{filterPhrase: search},
                                                   companyID=request.session.get('company', -1))
    return render(request, 'manager/editPersonel.html', context)


def editVehicles(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')
    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'vehicles': Vehicle.objects.filter(companyID=request.session.get('company', -1)).order_by("VIN")
    }
    search = request.GET.get("phrase", None)
    if search is None:
        context['vehicles'] = Vehicle.objects.filter(
            companyID=request.session.get('company', -1))
    else:
        filter = request.GET.get("filter", None)
        filterPhrase = filter + '__icontains'
        context['vehicles'] = Vehicle.objects.filter(**{filterPhrase: search},
                                                     companyID=request.session.get('company', -1))
    return render(request, 'manager/editVehicles.html', context)


def editVehicle(request, vid):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    obj = get_object_or_404(Vehicle, VIN=vid)
    vehicle = obj
    context = {
        'vehicle': vehicle,
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }

    return render(request, 'manager/editVehicle.html', context)


def vehicle_update_view(request, uvid):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    vehicle = Vehicle.objects.filter(VIN=uvid).first()
    form = VehiclesForm(request.POST or None, request.FILES, instance=vehicle)
    context = {
        'vehicle': vehicle,
        'vehicles': Vehicle.objects.filter(companyID=request.session.get('company', -1)).order_by("VIN"),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }

    if form.is_valid():
        post = form.save(commit = False)
        saveChangeLog(id=request.session.get('company', -1),
                post=post, name="changed", obj2 = post, obj = Vehicle.objects.filter(VIN=post.VIN).first())
        post.save()
        return render(request, "manager/editVehicles.html", context)
    return render(request, "manager/editVehicle.html", context)


def editService(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editService.html', context)


def editServiceplan(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editServiceplan.html', context)


def editPlans(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager'),
    }
    search = request.GET.get("phrase", None)
    if search is None:
        context['serviceplans'] = Serviceplan.objects.all().order_by(
            'brand', 'model', 'version', 'accessories')
    else:
        filter = request.GET.get("filter", None)
        filterPhrase = filter + '__icontains'
        context['serviceplans'] = Serviceplan.objects.filter(
            **{filterPhrase: search}).order_by('brand', 'model', 'version', 'accessories')

    return render(request, 'manager/editPlans.html', context)


def updatePlan(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    id = request.POST.get('id')
    print(id)
    serviceplan = Serviceplan.objects.filter(id=id).first()
    print(serviceplan)
    form = ServiceplanForm(request.POST or None, instance=serviceplan)
    context = {
        'plan': serviceplan,
        'serviceplans': Serviceplan.objects.all().order_by('brand', 'model', 'version', 'accessories', 'date'),
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }
    if form.is_valid():
        post = form.save()
        saveLog(id=request.session.get('company', -1),
                post=post, name="changed")
        return render(request, "manager/editServiceplan.html", context)
    print(form.is_valid)
    print(form.errors)
    return render(request, "manager/editPlans.html", context)


def saveLog(name, id, post):
    f = open("logFile.txt", "a")
    logDate = datetime.datetime.now()
    f.write("{} was {} by company id = {} date = {}\n".format(
        post, name, id, logDate.strftime("%x %X")))
    f.close()


def saveChangeLog(name, id, post, obj, obj2):
    f = open("logFile.txt", "a")
    logDate = datetime.datetime.now()
    differences = findDiff(obj, obj2)
    f.write("{} was {} by company id = {} date = {}\n".format(
        post, name, id, logDate.strftime("%x %X")))
    f.write("{}\n".format(len(differences)))
    for diff in differences:
        f.write("{} before: {} now: {}\n".format(diff, getattr(obj, diff), getattr(obj2, diff)))
    f.close()


def rentalLog(name, person, post, companyId):
    f = open("rentalLog.txt", "a")
    logDate = datetime.datetime.now()
    f.write("{} was {} by company id = {}, person id = {} date = {}\n".format(
        post, name, companyId, person.ID, logDate.strftime("%x %X")))
    f.close()


def generateReport(request):

    if request.session.get('currentUser', 'none') != 'admin':
        return redirect('login')


    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    f = open("logFile.txt", 'r')
    text = f.readlines()

    textobject = p.beginText()
    textobject.setTextOrigin(10, 830)
    textobject.setFont('Times-Roman', 12)
    i = 0
    while  i < len(text):
        companyID = re.search("company id = \d+", text[i])
        if request.session.get('id', -1) == int(companyID[0][13:]):

            if re.search("Person object", text[i]) is not None:

                personID = re.search("\(\d+\)", text[i])

                person = Person.objects.filter(
                    ID=int(personID[0][1:-1])).first()

                textobject.textLine("{} {} {} {}".format(
                    text[i][:personID.start()], person.name, person.surname, text[i][personID.start():]))

            else:
                vehicleVIN = re.search("\(\w+\)", text[i])
                vehicle = Vehicle.objects.filter(
                    VIN=vehicleVIN[0][1:-1]).first()
                textobject.textLine("{} {} {} {}".format(
                    text[i][:vehicleVIN.start()], vehicle.brand, vehicle.model, text[i][vehicleVIN.start():]))
            operation = re.search("was \w+ by", text[i])
            if text[i][operation.start():operation.end()] == "was changed by":
                 i += 1
                 j = int(text[i])
                
                 for k in range(0, j):
                    i += 1    
                    textobject.textLine("{}".format(text[i]))
            i += 1
            textobject.textLine("")

    p.drawText(textobject)
    p.showPage()
    p.save()

    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    pdf2 = generateRentalReport(request.session.get('id', -1))
    response = HttpResponse(content_type='application/zip')
    zf = zipfile.ZipFile(response, 'w')
    #zf.writestr("Report {}.pdf".format(datetime.datetime.now().strftime("%x %X")), pdf)
    zf.writestr("Report.pdf", pdf)
    zf.writestr("RentalReport.pdf", pdf2)
    return response
    #return FileResponse(buffer, as_attachment=True, filename="Report {}.pdf".format(datetime.datetime.now().strftime("%x %X")))



def generateRentalReport(companyId):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    f = open("rentalLog.txt", 'r')
    text = f.readlines()

    textobject = p.beginText()
    textobject.setTextOrigin(10, 830)
    textobject.setFont('Times-Roman', 12)

    for line in text:
        companyID = re.search("company id = \d+", line)
        if companyId == int(companyID[0][13:]):

            rentalID = re.search("\(\d+\)", line)

            rental = Rental.objects.filter(
                rent_id=int(rentalID[0][1:-1])).first()

            coma = re.search(",", line)

            type = re.search("was \w+ by", line)

            textobject.textLine("{} dates from: {} to: {} ".format(
                line[:rentalID.end()], rental.rent_start, rental.rent_end))

            textobject.textLine("renter: {} {} vehicle: {} {} {}".format(
                rental.renter_id.name, rental.renter_id.surname,  rental.vehicle_id.VIN, rental.vehicle_id.model, rental.vehicle_id.brand))

            textobject.textLine("{} {} ".format(
                line[type.start(): type.end()], line[coma.end()+1:]))

            textobject.textLine("")

    p.drawText(textobject)
    p.showPage()
    p.save()

    buffer.seek(0)
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
    #return FileResponse(buffer, as_attachment=True, filename="Rental Report {}.pdf".format(datetime.datetime.now().strftime("%x %X")))


def findDiff(obj1, obj2):
    fields = [field.name for field in obj1._meta.get_fields()]

    diff = []
    for field in fields:
        try:
            if getattr(obj1, field) != getattr(obj2, field):
                diff.append(field)
                print(field)
        except AttributeError:
            pass

    return diff
