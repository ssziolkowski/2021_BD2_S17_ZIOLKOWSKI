from django.db import models
from django.db.models import Deferrable, UniqueConstraint
from datetime import date


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    NIP = models.IntegerField()
    name = models.TextField()
    login = models.TextField(default="company", unique=True)
    password = models.TextField(default="password", unique=True)
    address = models.TextField()
    phone_number = models.TextField()
    domain = models.TextField()


class Person(models.Model):
    EMPLOYED = 'employed'
    DISCHARGED = 'discharged'
    STATUS = [
        (EMPLOYED, ('Currently employed')),
        (DISCHARGED, ('This worker is no longer employed'))
    ]
    ID = models.AutoField(primary_key=True)
    companyID = models.ForeignKey(
        Company, on_delete=models.RESTRICT, default=1)
    name = models.TextField()
    surname = models.TextField()
    phone_number = models.TextField()
    position = models.TextField()
    address = models.TextField()
    login = models.TextField(default="user", unique=True)
    password = models.TextField(default="password", unique=True)
    salary = models.IntegerField()
    status = models.TextField(choices=STATUS)


class Vehicle(models.Model):
    OPERATIONAL = 'operational'
    DISCHARGED = 'discharged'
    STATUS = [
        (OPERATIONAL, ('Currently operational')),
        (DISCHARGED, ('This vehicle is no longer operational'))
    ]
    VIN = models.TextField(primary_key=True)
    brand = models.TextField()
    version = models.TextField()
    model = models.TextField()
    category = models.TextField(default='other')
    accessories = models.TextField()
    picture = models.ImageField(upload_to='uploads/')
    companyID = models.ForeignKey(Company, on_delete=models.RESTRICT)
    plate_number = models.TextField()
    current_mileage = models.IntegerField(default=0)
    purpose = models.TextField()
    distinctive_marks = models.TextField()
    status = models.TextField(choices=STATUS)


class Manager(models.Model):
    personal_ID = models.ForeignKey(
        Person, related_name='%(class)s', on_delete=models.SET_NULL, null=True)
    VIN = models.ForeignKey(
        Vehicle, related_name='%(class)s', on_delete=models.SET_NULL, null=True)
    date_start = models.DateField(default=date.today)
    date_end = models.DateField()


class Rental(models.Model):
    PRIVATE = 'private'
    BUISNESS = 'buisness'
    STATUS = [
        (PRIVATE, ('Borrowed for private purposes')),
        (BUISNESS, ('Borrowed for buisness purposes'))
    ]
    rent_id = models.AutoField(primary_key=True)
    rent_type = models.TextField(choices=STATUS)
    renter_id = models.ForeignKey(Person, on_delete=models.RESTRICT)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)
    starting_mileage = models.IntegerField()
    final_mileage = models.IntegerField()
    exploitation_cost = models.FloatField()
    costs_description = models.TextField()
    rent_start = models.DateField()
    rent_end = models.DateField()
    rent_status = models.BooleanField(default=False)


class Service(models.Model):
    work_id = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)
    cost = models.FloatField()
    date = models.DateField(default=date.today)
    service_performed = models.TextField()
    provider = models.TextField()


class Serviceplan(models.Model):
    UniqueConstraint(fields=['brand', 'model', 'version',
                     'accessories'], name='serviceplan_id')
    brand = models.ForeignKey(
        Vehicle, related_name='%(class)s_brand', on_delete=models.RESTRICT)
    model = models.ForeignKey(
        Vehicle, related_name='%(class)s_model', on_delete=models.RESTRICT)
    version = models.ForeignKey(
        Vehicle, related_name='%(class)s_version', on_delete=models.RESTRICT)
    accessories = models.ForeignKey(
        Vehicle, related_name='%(class)s_accessories', on_delete=models.RESTRICT)
    service_performed = models.TextField()
    mileage = models.IntegerField()
    date = models.DateField(default=date.today)
    status = models.BooleanField()
