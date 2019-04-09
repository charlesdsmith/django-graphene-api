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
    adesa_id = models.CharField(max_length=20, default="n/a")


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
    html = models.TextField(blank=True, default="Check Online")
    origin_country = models.CharField(max_length=250, default="Check Online")
    run_date = models.CharField(max_length=20, default="Check Online")

class GetRecalls(models.Model):
    make = models.CharField(max_length=20, default="Check Online")
    vin = models.CharField(max_length=20)
    recalls = models.TextField(max_length=None, default="Check online")
    run_date = models.CharField(max_length=20, default="Check Online")



class GetAdesaRunList(models.Model):
    vin = models.CharField(max_length=20)
    img_url = models.URLField(blank=True)
    year = models.CharField(max_length=20, default="Check Online")
    make = models.CharField(max_length=20, default="Check Online")
    model = models.CharField(max_length=20, default="Check Online")
    grade = models.CharField(max_length=20, default="Check Online")
    colour = models.CharField(max_length=20, default="Check Online")
    MMR = models.TextField(default="{error: error}")
    run_date = models.CharField(max_length=20, default="Check Online")
    timestamp = models.DateTimeField(auto_now=True)  # updated timestamp
    lane = models.CharField(max_length=10, default="Check Online")
    trim = models.CharField(max_length=60, default="Check Online")
    mileage = models.CharField(max_length=20, default="Check Online")
    suggested_retail = models.TextField(default="{error: error}")
    human_valuation = models.TextField(default="0")
    run_no = models.CharField(max_length=20, default="Check Online")
    adesa_id = models.CharField(max_length=20, default="n/a")
    engine = models.TextField(default="n/a")
    transmission = models.CharField(max_length=20, default="n/a")
    wheel_drive = models.CharField(max_length=50, default="n/a")
    interior_color = models.CharField(max_length=50, default="n/a")
    total_damages = models.CharField(max_length=50, default="n/a")
    auction_location = models.CharField(max_length=50, default="n/a")
    check = models.TextField(default="n/a")
    extra = models.TextField(max_length=50, default="n/a")

    class Meta:
        ordering = ['id']


class ShoppingList(models.Model):
    vin = models.CharField(max_length=20)
    img_url = models.URLField()
    year = models.CharField(max_length=20, default="Check Online")
    make = models.CharField(max_length=20, default="Check Online")
    model = models.CharField(max_length=20, default="Check Online")
    grade = models.CharField(max_length=20, default="Check Online")
    colour = models.CharField(max_length=20, default="Check Online")
    MMR = models.TextField(default="{error: error}")
    check = models.TextField(default="n/a")
    run_date = models.CharField(max_length=20, default="Check Online")
    timestamp = models.DateTimeField(auto_now=True)  # updated timestamp
    lane = models.CharField(max_length=10, default="Check Online")
    trim = models.CharField(max_length=60, default="Check Online")
    mileage = models.CharField(max_length=20, default="Check Online")
    suggested_retail = models.CharField(max_length=250, default="{error: error}")
    human_valuation = models.TextField(default="0")
    run_no = models.CharField(max_length=20, default="Check Online")
    adesa_id = models.CharField(max_length=20, default="n/a")
    engine = models.TextField(default="n/a")
    transmission = models.CharField(max_length=20, default="n/a")
    wheel_drive = models.CharField(max_length=50, default="n/a")
    interior_color = models.CharField(max_length=50, default="n/a")
    total_damages = models.CharField(max_length=50, default="n/a")
    auction_location = models.CharField(max_length=50, default="n/a")
    check = models.TextField(default="n/a")
    extra = models.TextField(max_length=50, default="n/a")

    class Meta:
        ordering = ['id']


