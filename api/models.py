# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status, viewsets
from django.db import models
from django.utils import timezone

import time

# Create your models here.
class GetAdesaPurchases(models.Model):

    vin = models.CharField(max_length=20, null=False)
    vehicle_id = models.IntegerField(null=True)
    vehicle_make = models.CharField(max_length=20, null=True)
    vin_sticker = models.CharField(max_length=20, null=True)
    auction_id = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    model_name = models.CharField(max_length=20, null=True)
    mileage = models.IntegerField(null=True)
    unit_of_measurement = models.CharField(max_length=20, null=True)
    exterior_color = models.CharField(max_length=10, null=True)
    seller_name = models.CharField(max_length=20, null=True)
    purchase_date = models.DateTimeField(null=False)
    title_status = models.CharField(max_length=20, null=True)
    pdi_status = models.CharField(max_length=20, null=True)
    transport_status = models.CharField(max_length=20, null=True)
    location_name = models.CharField(max_length=20, null=True)
    buyer_rep_name = models.CharField(max_length=20, null=True)
    buyer_fee = models.CharField(max_length=20, null=True)
    buyer_ad_and_other_fees = models.CharField(max_length=20, null=True)
    fees_hst = models.CharField(max_length=20, null=True)
    taxable_purchase_price = models.CharField(max_length=20, null=True)
    total_hst = models.CharField(max_length=20, null=True)
    total_price = models.CharField(max_length=20, null=True)
    last_update_date_adesa = models.DateTimeField(null=True)
    last_update_date_gsm = models.DateTimeField(null=True)
    void_boolean = models.NullBooleanField(max_length=10)
    payment_status = models.CharField(max_length=10, null=True)
    amount = models.CharField(max_length=20, null=True)
    purchase_price = models.CharField(max_length=20, null=True)
    purchase_hst = models.CharField(max_length=20, null=True)
    bill_of_sale = models.URLField(null=True)
    checked = models.CharField(max_length=15, null=True)
    recalls = models.TextField(null=True)
    manufacturer_date = models.CharField(max_length=20, null=True)
    gvwr = models.CharField(max_length=20, null=True)
    gross_axle_weight_front = models.CharField(max_length=20, null=True)
    gross_axle_weight_rear = models.CharField(max_length=20, null=True)
    tire_size = models.CharField(max_length=20, null=True)
    tire_pressure_front = models.CharField(max_length=20, null=True)
    tire_pressure_rear = models.CharField(max_length=20, null=True)
    rim_size = models.CharField(max_length=20, null=True)


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

