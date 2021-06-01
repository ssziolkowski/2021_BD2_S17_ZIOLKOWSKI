import io
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


def managerPanel(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', '')
    }
    return render(request, 'manager/managerPanel.html', context)


def fleetManager(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

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
        post = form.save()
        saveLog(id=request.session.get('company', -1),
                post=post, name="changed")
        return render(request, "manager/editPersonel.html", context)

    return render(request, "manager/editPerson.html", context)


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
            form.save()
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
            form.save()
            rental = form.save(commit=False)
            rental.renter_id = Person.objects.filter(
                ID=request.session.get('id', -1)).first()
            rental.save()
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
            form.save()
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
            form.save()
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
            form.save()
            serviceplan = form.save(commit=False)
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


def updatePerson(request, pid):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editPersonel.html', context)


def editPersonel(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager'),
        'persons': Person.objects.filter(companyID=request.session.get('company', -1)).order_by("ID")
    }
    return render(request, 'manager/editPersonel.html', context)


def editVehicle(request):
    if request.session.get('currentUser', 'none') == 'none':
        return redirect('login')

    context = {
        'user': request.session.get('currentUser', 'none'),
        'name': request.session.get('name', 'FleetManager')
    }
    return render(request, 'manager/editVehicle.html', context)


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


def saveLog(name, id, post):
    f = open("logFile.txt", "a")
    logDate = datetime.datetime.now()
    f.write("{} was {} by company id = {} date = {}\n".format(
        post, name, id, logDate.strftime("%x %X")))
    f.close()


def generateReport(request):

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    f = open("logFile.txt", 'r')
    text = f.readlines()

    textobject = p.beginText()
    textobject.setTextOrigin(10, 830)
    textobject.setFont('Times-Roman', 12)

    for line in text:
        companyID = re.search("company id = \d+", line)
        if request.session.get('id', -1) == int(companyID[0][13:]):
            if re.search("Person object", line) is not None:

                personID = re.search("\(\d+\)", line)

                person = Person.objects.filter(
                    ID=int(personID[0][1:-1])).first()

                textobject.textLine("{} {} {} {}".format(
                    line[:personID.start()], person.name, person.surname, line[personID.start():]))

            else:
                personID = re.search("\(\d+\)", line)

                vehicleVIN = re.search("\(\w+\)", line)
                vehicle = Vehicle.objects.filter(
                    VIN=vehicleVIN[0][1:-1]).first()
                textobject.textLine("{} {} {} {}".format(
                    line[:personID.start()], vehicle.brand, vehicle.model, line[personID.start():]))

    p.drawText(textobject)
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="Report {}.pdf".format(datetime.datetime.now().strftime("%x %X")))
