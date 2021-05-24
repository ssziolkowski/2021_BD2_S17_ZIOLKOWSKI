from django import urls
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^Vehicles/(?P<ovin>[\w]+)/$', views.object_specific_view, name='Vehicle'),
    path('', views.fleetManager, name='fleetManager'),
    path('allVehicles', views.allVehicles, name='allVehicles'),
    path('addVehicle', views.addVehicle, name='addVehicle'),
    path('login', views.login, name='login'),
    path('rentVehicle', views.rentVehicle, name='rentVehicle'),
    path('selectedVehicle', views.selectedVehicle, name='selectedVehicle'),
    path('adminpanel', views.adminpanel, name='adminpanel'),
    path('addperson', views.addperson, name='addperson'),
    path('addservice', views.addservice, name='addservice'),
    path('addserviceplan', views.addserviceplan, name='addserviceplan'),
    path('editperson', views.editperson, name='editperson'),
    path('editvehicle', views.editvehicle, name='editvehicle'),
    path('editservice', views.editservice, name='editservice'),
    path('editserviceplan', views.editserviceplan, name='editserviceplan')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
