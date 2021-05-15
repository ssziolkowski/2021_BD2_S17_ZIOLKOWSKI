from django.db import models
from datetime import date

"""
class Person(models.Model):
    EMPLOYED = 'employed'
    DISCHARGED = 'discharged'
    STATUS = [
        (EMPLOYED, ('Currently employed')),
        (DISCHARGED, ('This worker is no longer employed'))
    ]
    ID = models.AutoField()
    name = models.TextField()
    surname = models.TextField()
    phone_number = models.TextField()
    position = models.TextField()
    address = models.TextField()
    salary = models.IntegerField(default=0)
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
    model = models.TextField()
    version = models.TextField()
    accessories = models.TextField()
    plate_number = models.TextField()
    current_mileage = models.IntegerField(default=0)
    propose = models.TextField()
    manager_id = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True)
    status = models.TextField(choices=STATUS)


class Rental(models.Model):
    PRIVATE = 'private'
    BUISNESS = 'buisness'
    STATUS = [
        (PRIVATE, ('Borrowed for private purposes')),
        (BUISNESS, ('Borrowed for buisness purposes'))
    ]
    rent_id = models.AutoField()
    rent_type = models.TextField(choices=STATUS)
    renter_id = models.ForeignKey(Person, on_delete=models.RESTRICT)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)
    starting_mileage = models.IntegerField()
    final_mileage = models.IntegerField()
    exploitation_cost = models.FloatField()
    costs_description = models.TextField()
    rent_start = models.DateField()
    rent_end = models.DateField()


class Service(models.Model):
    work_id = models.AutoField()
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)
    cost = models.FloatField()
    date = models.DateField(default=date.today)
    service_performed = models.TextField()
    provider = models.TextField()
"""
