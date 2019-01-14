# serialize the models here
from rest_framework import serializers
from django.core import serializers as django_serializer
from django.http import HttpResponse
from .models import GetAdesaPurchases, CarFax, GetRecalls, GetAdesaRunList, ShoppingList
import json
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetAdesaPurchases
        fields = ('vin', 'vehicle_id', 'vehicle_make', 'vin_sticker',
                  'auction_id', 'year', 'model_name', 'mileage',
                  'unit_of_measurement', 'exterior_color', 'seller_name',
                  'purchase_date', 'title_status', 'pdi_status',
                  'transport_status', 'location_name', 'buyer_rep_name',
                  'buyer_fee', 'buyer_ad_and_other_fees',
                  'fees_hst', 'taxable_purchase_price', 'total_hst', 'total_price',
                  'last_update_date_adesa', 'last_update_date_gsm',
                  'void_boolean', 'payment_status',
                  'amount', 'purchase_price', 'purchase_hst', 'bill_of_sale',
                  'checked', 'recalls', 'manufacturer_date', 'gvwr', 'gross_axle_weight_front',
                  'gross_axle_weight_rear', 'tire_size','tire_pressure_front',
                  'tire_pressure_rear', 'rim_size')

    def create(self, validated_data):
        return GetAdesaPurchases.objects.create(**validated_data)

class PurchasesBulkUploadSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = GetAdesaRunList
        fields = ('vin', 'vehicle_id', 'vehicle_make', 'vin_sticker',
                  'auction_id', 'year', 'model_name', 'mileage',
                  'unit_of_measurement', 'exterior_color', 'seller_name',
                  'purchase_date', 'title_status', 'pdi_status',
                  'transport_status', 'location_name', 'buyer_rep_name',
                  'buyer_fee', 'buyer_ad_and_other_fees',
                  'fees_hst', 'taxable_purchase_price', 'total_hst', 'total_price',
                  'last_update_date_adesa', 'last_update_date_gsm',
                  'void_boolean', 'payment_status',
                  'amount', 'purchase_price', 'purchase_hst', 'bill_of_sale',
                  'checked', 'recalls', 'manufacturer_date', 'gvwr', 'gross_axle_weight_front',
                  'gross_axle_weight_rear', 'tire_size','tire_pressure_front',
                  'tire_pressure_rear', 'rim_size')
        list_serializer_class = BulkListSerializer


class CarFaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarFax
        fields = ('vin', 'structural_damage', 'total_loss',
                  'accident', 'airbags', 'odometer', 'recalls',
                  'last_updated', 'origin_country', 'html', 'run_date')

    def create(self, validated_data):
        print(validated_data)
        return CarFax.objects.create(**validated_data)

class CarFaxBulkUploadSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CarFax
        fields = ('vin', 'structural_damage', 'total_loss',
                   'accident', 'airbags', 'odometer', 'recalls',
                   'last_updated', 'origin_country', 'html', 'run_date')
        list_serializer_class = BulkListSerializer


class RecallsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GetRecalls
        # can also use "fields = '__all__'" but it will include the objects id too
        fields = ("vin", "make", "recalls", "run_date")

    def create(self, validated_data):
        return GetRecalls.objects.create(**validated_data)

class RecallsBulkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetRecalls
        # can also use "fields = '__all__'" but it will include the objects id too
        fields = ("vin", "make", "recalls", "run_date")

    def create(self, validated_data):
        return GetRecalls.objects.create(**validated_data)

class AdesaRunlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetAdesaRunList
        fields = ('vin', 'img_url', 'year', 'make', 'model', 'grade',
                  'colour', 'MMR', 'MID', 'GSMR', 'transactions', 'run_date', 'timestamp', 'lane', 'trim', 'mileage')


    def create(self, validated_data):
        # check to see if object with 'vin' value exists, if it does and
        # has a  different run_date, overwrite
        '''try:
            test = django_serializer.serialize("json", GetAdesaRunList.objects.filter(vin=validated_data["vin"]))
            for obj in json.loads(test):
                if obj["fields"]["run_date"] == validated_data["run_date"]:
                    print('found one')
                    print(type(obj))
                    return GetAdesaRunList.objects.get
                else:
                    print('else create')
                    print(obj["fields"]["run_date"])
                    return GetAdesaRunList.objects.create(**validated_data)

        except Exception as e:
            # if a record with that vin isn't already in the database, just create it
            #test = django_serializer.serialize("json", GetAdesaRunList.objects.filter(vin='123456'))
            print(e)
            print('except create')
            return GetAdesaRunList.objects.create(**validated_data)'''
        return GetAdesaRunList.objects.create(**validated_data)

class AdesaRunListBulkUploadSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = GetAdesaRunList
        fields = ('vin', 'img_url', 'year', 'make', 'model', 'grade',
                  'colour', 'MMR', 'MID', 'GSMR', 'transactions', 'run_date', 'timestamp', 'lane', 'trim',
                  'mileage', 'suggested_retail')
        list_serializer_class = BulkListSerializer


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('vin', 'img_url', 'year', 'make', 'model', 'grade',
                  'colour', 'MMR', 'MID', 'GSMR', 'transactions', 'run_date', 'timestamp', 'lane',
                  "suggested_retail")

    def create(self, validated_data):
        '''try:
            test = django_serializer.serialize("json", GetRecalls.objects.filter(vin=validated_data["vin"]))
            for obj in test:
                if obj["fields"]["run_date"] == validated_data["run_date"]:
                    return "That record already exists with that run_date, not uploading to database"
                else:
                    return GetRecalls.objects.create(**validated_data)

        except:
            # if a record with that vin isn't already in the database, just create it
            return GetRecalls.objects.create(**validated_data)'''
        return ShoppingList.objects.create(**validated_data)
