# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status, viewsets
from django.db import models
from django.utils import timezone
from graphene_django import DjangoObjectType
import graphene

import time

# Create your models here.
class GetAdesaPurchases(models.Model):

    vin = models.CharField(max_length=20, null=False)
    vehicle_id = models.IntegerField()
    vehicle_make = models.CharField(max_length=20, default="n/a")
    vin_sticker = models.CharField(max_length=20, default="n/a")
    auction_id = models.IntegerField()
    year = models.IntegerField()
    model_name = models.CharField(max_length=20, default="n/a")
    mileage = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=20, default="n/a")
    exterior_color = models.CharField(max_length=10, default="n/a")
    seller_name = models.CharField(max_length=20, default="n/a")
    purchase_date = models.DateTimeField(null=True)
    title_status = models.CharField(max_length=20, default="n/a")
    pdi_status = models.CharField(max_length=20, default="n/a")
    transport_status = models.CharField(max_length=20, default="n/a")
    location_name = models.CharField(max_length=20, default="n/a")
    buyer_rep_name = models.CharField(max_length=20, default="n/a")
    buyer_fee = models.CharField(max_length=20, default="n/a")
    buyer_ad_and_other_fees = models.CharField(max_length=20, default="n/a")
    fees_hst = models.CharField(max_length=20, default="n/a")
    taxable_purchase_price = models.CharField(max_length=20, default="n/a")
    total_hst = models.CharField(max_length=20, default="n/a")
    total_price = models.CharField(max_length=20, default="n/a")
    last_update_date_adesa = models.DateTimeField(null=True)
    last_update_date_gsm = models.DateTimeField(null=True)
    void_boolean = models.NullBooleanField(max_length=10)
    payment_status = models.CharField(max_length=10, default="n/a")
    amount = models.CharField(max_length=20, default="n/a")
    purchase_price = models.CharField(max_length=20, default="n/a")
    purchase_hst = models.CharField(max_length=20, default="n/a")
    bill_of_sale = models.URLField(default="n/a")
    checked = models.CharField(max_length=15, default="n/a")
    recalls = models.TextField(default="n/a")
    manufacturer_date = models.CharField(max_length=20, default="n/a")
    gvwr = models.CharField(max_length=20, default="n/a")
    gross_axle_weight_front = models.CharField(max_length=20, default="n/a")
    gross_axle_weight_rear = models.CharField(max_length=20, default="n/a")
    tire_size = models.CharField(max_length=20, default="n/a")
    tire_pressure_front = models.CharField(max_length=20, default="n/a")
    tire_pressure_rear = models.CharField(max_length=20, default="n/a")
    rim_size = models.CharField(max_length=20, default="n/a")


# totalLossCells, frameDamageCells, airbagCells, odometerCells, accidentCheckCells, recallCells
class CarFax(models.Model):
    vin = models.CharField(max_length=20)
    structural_damage = models.CharField(max_length=100, default="Check Online")
    total_loss = models.CharField(max_length=100, default="Check Online")
    accident = models.CharField(max_length=100, default="Check Online")
    airbags = models.CharField(max_length=100, default="Check Online")
    odometer = models.CharField(max_length=100, default="Check Online")
    recalls = models.CharField(max_length=100, default="Check Online")
    last_updated = models.DateTimeField(auto_now=True)  # updated timestamp
    html = models.TextField(max_length=None, default="Check Online")
    origin_country = models.CharField(max_length=15, default="Check Online")
    run_date = models.CharField(max_length=20, default="Check Online")

class GetRecalls(models.Model):
    make = models.CharField(max_length=20, default="Check Online")
    vin = models.CharField(max_length=20)
    recalls = models.TextField(max_length=None, default="Check online")
    run_date = models.CharField(max_length=20, default="Check Online")


class GetAdesaRunList(models.Model):
    vin = models.CharField(max_length=20)
    img_url = models.URLField()
    year = models.IntegerField()
    make = models.CharField(max_length=20, default="Check Online")
    model = models.CharField(max_length=20, default="Check Online")
    grade = models.IntegerField(default="Check Online")
    colour = models.CharField(max_length=20, default="Check Online")
    MMR = models.TextField(max_length=50, default="Check Online")
    MID = models.CharField(max_length=20, default="Check Online")
    GSMR = models.TextField(max_length=50, default="Check Online")
    transactions = models.CharField(max_length=20, default="Check Online")
    run_date = models.CharField(max_length=20, default="Check Online")
    timestamp = models.DateTimeField(auto_now=True)  # updated timestamp

class ShoppingList(models.Model):
    vin = models.CharField(max_length=20)
    img_url = models.URLField()
    year = models.IntegerField()
    make = models.CharField(max_length=20, default="Check Online")
    model = models.CharField(max_length=20, default="Check Online")
    grade = models.IntegerField(default="Check Online")
    colour = models.CharField(max_length=20, default="Check Online")
    MMR = models.TextField(max_length=50, default="Check Online")
    MID = models.CharField(max_length=20, default="Check Online")
    GSMR = models.TextField(max_length=50, default="Check Online")
    transactions = models.CharField(max_length=20, default="Check Online")
    run_date = models.CharField(max_length=20, default="Check Online")
    timestamp = models.DateTimeField(auto_now=True)  # updated timestamp


#### GraphQL ####
class CarFaxType(DjangoObjectType):
    class Meta:
        model = CarFax

class RecallsType(DjangoObjectType):
    class Meta:
        model = GetRecalls

class Query(graphene.ObjectType):
    all_carfax_objects = graphene.List(CarFaxType)
    all_recalls_type = graphene.List(RecallsType)

    def return_all_carfax(self, info, **kwargs):
        return CarFax.objects.all()

    def return_all_recalls(self, info, **kwargs):
        return GetRecalls.objects.all()

schema = graphene.Schema(query=Query)

query = '''
query {
    return_all_carfax {
        vin,
        accident
    }
}
'''

result = schema.execute(query)