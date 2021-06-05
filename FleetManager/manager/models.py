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
    DECOMMISSIONED = 'decommissioned'
    STATUS = [
        (OPERATIONAL, ('Currently operational')),
        (DECOMMISSIONED, ('This vehicle is no longer operational'))
    ]
    SEDAN = 'sedan'
    WAGON = 'wagon'
    HATCHBACK = 'hatchback'
    VAN = 'van'
    PICKUP = 'pickup'
    TRUCK = 'truck'
    CONSTRUCTION = 'construction'
    AGRICULTURE = 'agriculture'
    STORAGE = 'storage'
    OTHER = 'other'
    VEHICLECATEGORY = [
        (SEDAN, ('Sedan')),
        (WAGON, ('Wagon')),
        (HATCHBACK, ('Hatchback')),
        (VAN, ('Van')),
        (PICKUP, ('Pickup')),
        (TRUCK, ('Truck')),
        (CONSTRUCTION, ('Construction')),
        (AGRICULTURE, ('Agriculture')),
        (STORAGE, ('Storage')),
        (OTHER, ('Other'))
    ]
    VIN = models.TextField(primary_key=True)
    brand = models.TextField()
    version = models.TextField()
    model = models.TextField()
    category = models.TextField(choices=VEHICLECATEGORY)
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
    RESERVED = 'reserved'
    RENTED = 'rented'
    GIVEN = 'given'
    RENTSTATUS = [
        (RESERVED, ('Reserved for user')),
        (RENTED, ('Rented by user')),
        (GIVEN, ('Given by user'))
    ]
    rent_id = models.AutoField(primary_key=True)
    rent_type = models.TextField(choices=STATUS)
    renter_id = models.ForeignKey(Person, on_delete=models.RESTRICT, null=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)
    starting_mileage = models.IntegerField(null=True)
    final_mileage = models.IntegerField(null=True)
    exploitation_cost = models.FloatField(null=True)
    costs_description = models.TextField(null=True)
    rent_start = models.DateField()
    rent_end = models.DateField()
    rent_status = models.TextField(choices=RENTSTATUS)


class Serviceplan(models.Model):
    #id = models.AutoField(primary_key=True)
    UniqueConstraint(fields=['brand', 'model', 'version',
                     'accessories'], name='serviceplan_id')
    brand = models.TextField()
    model = models.TextField()
    version = models.TextField()
    accessories = models.TextField()
    service_performed = models.TextField()
    mileage = models.IntegerField()
    date = models.DateField(default=date.today)


class Service(models.Model):
    work_id = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)
    cost = models.FloatField()
    date = models.DateField(default=date.today)
    service_performed = models.TextField()
    provider = models.TextField()
    plan = models.ForeignKey(Serviceplan, on_delete=models.SET_NULL, null=True)
