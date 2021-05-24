from django.forms.fields import ImageField
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.utils import timezone
from django.utils.translation import templatize
from .models import Person, Service, Serviceplan, Vehicle, models
from django.utils.safestring import mark_safe


#class PictureWidget(forms.widgets.Widget):
   # def render(self, name, value, attrs=None):
       # html =  templatize("""<img src="$link"/>""")
      #  return mark_safe(html.substitute(link=value))


class VehiclesForm(forms.ModelForm):
    #picture = ImageField(widget=PictureWidget)
    
    class Meta:
        model = Vehicle
        fields = ('VIN', 'brand', 'version', 'model', 'accessories', 'plate_number', 'current_mileage', 'purpose','status','distinctive_marks','picture')
        pic_field = ('picture')


class PersonForm(forms.ModelForm):
    
    class Meta:
        model = Person
        fields = ('name', 'surname', 'phone_number', 'position', 'address', 'salary', 'status')


#TODO: validate vin 
class ServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = ('vehicle_id', 'cost', 'date', 'service_performed', 'provider')

class ServiceplanForm(forms.ModelForm):
    
    class Meta:
        model = Serviceplan
        fields = ('brand', 'version', 'model', 'accessories', 'date', 'service_performed', 'mileage', 'status')
