from django.forms.fields import ImageField
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.utils import timezone
from django.utils.translation import templatize
from .models import Person, Vehicle, models
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
