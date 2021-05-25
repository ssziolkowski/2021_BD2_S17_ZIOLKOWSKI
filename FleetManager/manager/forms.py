from django.forms.fields import ImageField
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.utils import timezone
from django.utils.translation import templatize
from .models import Person, Service, Serviceplan, Vehicle, models
from django.utils.safestring import mark_safe


class VehiclesForm(forms.ModelForm):
    
    class Meta:
        model = Vehicle
        fields = ('VIN', 'brand', 'version', 'model', 'accessories', 'plate_number', 'current_mileage', 'purpose','status','distinctive_marks','picture')
        pic_field = ('picture')


class PersonForm(forms.ModelForm):
    
    class Meta:
        model = Person
        #id_field = ("ID")
        fields = ('name', 'surname', 'phone_number', 'position', 'address', 'salary', 'status')


#TODO: validate vin with db
class ServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = ('vehicle_id', 'cost', 'date', 'service_performed', 'provider')


#TODO: validate wszystko with db
class ServiceplanForm(forms.ModelForm):
    
    class Meta:
        model = Serviceplan
        fields = ('brand', 'version', 'model', 'accessories', 'date', 'service_performed', 'mileage', 'status')
