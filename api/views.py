# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import GetAdesaPurchases, CarFax, GetRecalls
from .serializers import PurchasesSerializer, RecallsSerializer, CarFaxSerializer
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers, authentication
from rest_framework.decorators import action

# had to go online and download oauth2_provider manually, package installed oauth2_provider was missing files
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
from oauth2_provider.views.generic import ProtectedResourceView



# Create your views here.

class getAdesaPurchases(viewsets.ModelViewSet):
    ''' The actions provided by the ModelViewSet class are .list(), .retrieve(),
      .create(), .update(), .partial_update(), and .destroy(). '''

    queryset = GetAdesaPurchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def list(self, request):
        # accessed at url: ^api/v1/purchases/$
        queryset = GetAdesaPurchases.objects.all()
        serializer = PurchasesSerializer(queryset, many=True)
        print('here')

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
        print('here')

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        queryset = GetRecalls.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = RecallsSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)

    '''def create(self, request, **validated_data):
        serializer = PurchasesSerializer(GetAdesaPurchases.objects.create(**validated_data))
        headers = self.get_success_headers(serializer.data)

        print(headers)
        return Response(serializer.data, headers=headers)'''


class GetCarFax(viewsets.ModelViewSet):
    ''' This view will be used for GETing new carfax reports to the database '''

    required_scopes = ['write']  # necessary to specify what type of permission the token should have to access this endpoint
    queryset = CarFax.objects.all()
    serializer_class = CarFaxSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


    def list(self, request, **kwargs):

        # accessed at url: ^api/v1/carfax/$
        queryset = CarFax.objects.all()
        serializer = CarFaxSerializer(queryset, many=True)
        print(request.user)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # accessed at url: ^api/v1/retrieve/{pk}/$
        queryset = CarFax.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, vin__exact=pk)
        serializer = CarFaxSerializer(record, many=True)
        print('CARFAX RETRIEVE')

        return Response(serializer.data)

    def retrieve_by_rundate(self, request, rundate=None):
        # accessed at url: ^api/v1/retrieve/{pk}/$
        queryset = CarFax.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, rundate__exact=rundate)
        serializer = CarFaxSerializer(record, many=True)

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        queryset = CarFax.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = CarFaxSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)



class Recalls(viewsets.ModelViewSet):
    '''
    This view will be fore retrieving a recall for a car from the database
    '''


    queryset = GetRecalls.objects.all()
    serializer_class = RecallsSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    #lookup_field = "vin"



    def list(self, request, **kwargs):

        queryset = GetRecalls.objects.all()
        serializer = RecallsSerializer(queryset, many=True)
        print('LIST')

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):

        queryset = GetRecalls.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, vin__exact=pk)
        serializer = RecallsSerializer(record, many=True)


        print('RETRIEVE ONE')

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        queryset = GetRecalls.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = RecallsSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)
