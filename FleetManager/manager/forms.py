from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.utils import timezone
from .models import Person, Vehicle, models


class VehiclesForm(forms.ModelForm):

    pic_field = ('picture')
    class Meta:
        model = Vehicle
        fields = ('VIN', 'brand', 'version', 'model', 'accessories', 'plate_number', 'current_mileage', 'purpose','status','distinctive_marks')



