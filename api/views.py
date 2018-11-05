# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import GetAdesaPurchases, CarFax
from .serializers import PurchasesSerializer
from .serializers import CarFaxSerializer
from rest_framework.response import Response


# Create your views here.

class getAdesaPurchases(viewsets.ModelViewSet):
    ''' The actions provided by the ModelViewSet class are .list(), .retrieve(),
      .create(), .update(), .partial_update(), and .destroy(). '''

    queryset = GetAdesaPurchases.objects.all()
    serializer_class = PurchasesSerializer
    authentication_classes = []

    def list(self, request):
        # accessed at url: ^api/v1/purchases/$
        queryset = GetAdesaPurchases.objects.all()
        serializer = PurchasesSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # accessed at url: ^api/v1/purchases/{pk}/$

        queryset = GetAdesaPurchases.objects.all()
        # https://docs.djangoproject.com/en/2.1/topics/http/shortcuts/#get-object-or-404
        record = get_list_or_404(queryset, vin__exact=pk)
        # To serialize a queryset or list of objects instead of a single object instance,
        # you should pass the many=True flag when instantiating the serializer
        # https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-multiple-objects
        serializer = PurchasesSerializer(record, many=True)

        return Response(serializer.data)

    '''def create(self, request, **validated_data):
        serializer = PurchasesSerializer(GetAdesaPurchases.objects.create(**validated_data))
        headers = self.get_success_headers(serializer.data)

        print(headers)
        return Response(serializer.data, headers=headers)'''


class GetCarFax(viewsets.ModelViewSet):
    ''' This view will be used for POSTing new carfax reports to the database '''

    queryset = CarFax.objects.all()
    serializer_class = CarFaxSerializer
    # authentication_classes = []
    permission_classes = []
    #print('TEST')
    # lookup_field = "vin"


    def list(self, request):

        # accessed at url: ^api/v1/carfax/$
        queryset = CarFax.objects.all()
        serializer = CarFaxSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # accessed at url: ^api/v1/retrieve/{pk}/$
        queryset = CarFax.objects.all()
        record = get_list_or_404(queryset, vin__exact=pk)
        serializer = CarFaxSerializer(record, many=True)

        return Response(serializer.data)

    '''def create(self, request, **validated_data):
        print('TEST')
        # print(request.data)
        print(validated_data)
        serializer = CarFaxSerializer(CarFax.objects.create(**validated_data))
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)

        print(headers)
        return Response(serializer.data, headers=headers)'''

    #print(custom_exception_handler())