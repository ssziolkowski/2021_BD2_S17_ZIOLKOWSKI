from django.urls import path

from . import views

urlpatterns = [
    path('', views.fleetManager, name='fleetManager'),
    path('allVehicles', views.allVehicles, name='allVehicles'),
    path('addVehicle', views.addVehicle, name='addVehicle'),
    path('login', views.login, name='login'),
    path('rentVehicle', views.rentVehicle, name='rentVehicle'),
    path('selectedVehicle', views.selectedVehicle, name='selectedVehicle')
]
