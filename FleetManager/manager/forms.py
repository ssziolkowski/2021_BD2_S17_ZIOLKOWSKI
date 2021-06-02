from django.forms.fields import ImageField
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.utils import timezone
from django.utils.translation import templatize
from .models import Person, Rental, Service, Serviceplan, Vehicle, models
from django.utils.safestring import mark_safe


class LoginForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput())
    login = forms.CharField()


class VehiclesForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ('VIN', 'brand', 'version', 'model', 'accessories', 'plate_number',
                  'current_mileage', 'purpose', 'status', 'distinctive_marks', 'picture')
        pic_field = ('picture')


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('login', 'password', 'name', 'surname', 'phone_number',
                  'position', 'address', 'salary', 'status')


class ReserveForm(forms.ModelForm):

    class Meta:
        model = Rental
        fields = ('rent_type', 'rent_start', 'rent_end', 'vehicle_id')


# TODO: validate vin with db
class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ('vehicle_id', 'cost', 'date',
                  'service_performed', 'provider')


# TODO: validate wszystko with db
class ServiceplanForm(forms.ModelForm):

    class Meta:
        model = Serviceplan
        fields = ('model', 'version', 'accessories', 'brand',
                  'date', 'service_performed', 'mileage')
