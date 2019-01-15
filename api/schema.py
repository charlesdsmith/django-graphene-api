from graphene_django import DjangoObjectType
import graphene
from api.models import CarFax, GetRecalls, GetAdesaRunList, GetAdesaPurchases
from api.serializers import *
from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from django.shortcuts import get_object_or_404, get_list_or_404
from graphene_django.rest_framework.mutation import SerializerMutation


#### GraphQL ####
#  https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/#introduction-tutorial-graphene-and-django

class CarFaxType(DjangoObjectType):
    class Meta:
        model = CarFax
        interfaces = (Node, )

class RecallsType(DjangoObjectType):
    class Meta:
        model = GetRecalls
        interfaces = (Node, )

class Query(graphene.ObjectType):
    all_carfax_objects = graphene.List(CarFaxType)
    all_recalls_objects = graphene.List(RecallsType)

    carfax = graphene.Field(lambda: graphene.List(CarFaxType), vin=graphene.String(), run_date=graphene.String())
    recalls = graphene.Field(lambda: graphene.List(RecallsType), vin=graphene.String(), run_date=graphene.String())


    def resolve_all_carfax_objects(self, info, **kwargs):
        return CarFax.objects.all()

    def resolve_all_recalls_objects(self, info, **kwargs):
        return GetRecalls.objects.all()

    def resolve_carfax(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            return CarFax.objects.get(vin=vin)

        if run_date is not None:
            all_carfax_objects = CarFax.objects.filter(run_date__exact=run_date)
            return all_carfax_objects

        return None


    def resolve_recalls(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            return GetRecalls.objects.get(vin=vin)

        if run_date is not None:
            all_recalls_objects = GetRecalls.objects.filter(run_date__exact=run_date)
            return all_recalls_objects

        return None

class CarFaxMutation(SerializerMutation):
    class Meta:
        serializer_class = CarFaxSerializer

schema = graphene.Schema(query=Query, mutation=CarFaxMutation)

query = '''
query {
    allCarfaxObjects {
        vin,
        accident
    }
}
'''

result = schema.execute(query)

print(result)