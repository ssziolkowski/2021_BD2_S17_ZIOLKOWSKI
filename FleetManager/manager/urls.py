from django import urls
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^allVehicles/(?P<otype>[\w]+)/$',
        views.filterVehicle_view, name='VehicleFilter'),
    url(r'^editPerson/(?P<pid>[\w]+)/$', views.editPerson, name='editPerson'),
    url(r'^editVehicle/(?P<vid>[\w]+)/$', views.editVehicle, name='editVehicle'),
    url(r'^updatePerson/(?P<upid>[\w]+)/$',
        views.person_update_view, name='person_update_view'),
    url(r'^updateVehicle/(?P<uvid>[\w]+)/$',
        views.vehicle_update_view, name='vehicle_update_view'),
    path('', views.fleetManager, name='fleetManager'),
    path('allVehicles', views.allVehicles, name='allVehicles'),
    path('addVehicle', views.addVehicle, name='addVehicle'),
    path('login', views.login, name='login'),
    path('rentVehicle', views.rentVehicle, name='rentVehicle'),
    path('selectedVehicle', views.selectedVehicle_view,
         name='selectedVehicleView'),
    path('managedVehicle', views.managedVehicle, name='managedVehicle'),
    path('adminPanel', views.adminPanel, name='adminPanel'),
    path('addPerson', views.addPerson, name='addPerson'),
    path('addService', views.addService, name='addService'),
    path('addServiceplan', views.addServiceplan, name='addServiceplan'),
    path('editPerson', views.editPerson, name='editPerson'),
    path('editPersonel', views.editPersonel, name='editPersonel'),
    path('editVehicles', views.editVehicles, name='editVehicles'),
    path('editVehicle', views.editVehicle, name='editVehicle'),
    path('editService', views.editService, name='editService'),
    path('managerManager', views.managerManager, name='managerManager'),
    path('editServiceplan', views.editServiceplan, name='editServiceplan'),
    path('managerPanel', views.managerPanel, name='managerPanel'),
    path('generateReport', views.generateReport, name='generateReport'),
    path('reserveVehicle', views.reserveVehicle, name='reserveVehicle'),
    path('startRent', views.startRent, name='startRent'),
    path('endRent', views.endRent, name='endRent'),
    path('yourVehicles', views.yourVehiclesView, name='yourVehicles'),
    path('toStartRent', views.toStartRent, name='toStartRent'),
    path('toEndRent', views.toEndRent, name='toEndRent'),
    path('rentalDetails', views.rentalDetailsView, name='rentalDetails'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
