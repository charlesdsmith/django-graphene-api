# serialize the models here
from rest_framework import serializers
from .models import GetAdesaPurchases, CarFax, GetRecalls
from rest_framework.response import Response
from rest_framework.views import exception_handler


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


class CarFaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarFax
        fields = ('vin', 'structural_damage', 'total_loss',
                  'accident', 'airbags', 'odometer', 'recalls',
                  'last_updated', 'origin_country')

    def create(self, validated_data):
        print(validated_data)
        return CarFax.objects.create(**validated_data)

    '''def custom_exception_handler(exc):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
        response = exception_handler(exc)

        # Now add the HTTP status code to the response.
        if response is not None:
            response.data['status_code'] = response.status_code

        return response'''

class RecallsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GetRecalls
        # can also use "fields = '__all__'" but it will include the objects id too
        fields = ("vin", "make", "recalls", "run_date")

        print('RETRIEVE')

    def create(self, validated_data):
        return GetRecalls.objects.create(**validated_data)


