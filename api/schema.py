from graphene_django import DjangoObjectType
import graphene
from api.models import CarFax, GetRecalls, GetAdesaRunList, GetAdesaPurchases
from api.serializers import *
from graphene import ObjectType, Node, Schema, relay
from django.core.exceptions import ObjectDoesNotExist
from graphene_django.fields import DjangoConnectionField
from django.shortcuts import get_object_or_404, get_list_or_404
from graphene_django.rest_framework.mutation import SerializerMutation
# from types import ErrorType
import http

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

class AdesaPurchasesType(DjangoObjectType):
    class Meta:
        model = GetAdesaPurchases
        interfaces = (Node, )

class AdesaRunListType(DjangoObjectType):
    class Meta:
        model = GetAdesaRunList
        interfaces = (Node, )

class ShoppingListType(DjangoObjectType):
    class Meta:
        model = ShoppingList
        interfaces = (Node, )

class CarFaxInput(graphene.InputObjectType):
    vin = graphene.String(required=True)

class AdesaRunlistInput(graphene.InputObjectType):
    vin = graphene.String(required=True)
    run_date = graphene.String(required=True)
    human_valuation = graphene.String(required=True)

class ShoppingListInput(graphene.InputObjectType):
    vin = graphene.String(required=True)
    run_date = graphene.String(required=True)
    human_valuation = graphene.String(required=True)


'''class CreateCarFax(graphene.Mutation):
    class Arguments:
        # Arguments attributes are the arguments that the mutation needs for resolving
        vin = CarFaxInput(required=True)

    carfax = graphene.Field(CarFax)

    # mutate is the function that will be applied once the mutation is called
    @staticmethod
    def mutate(self, info, vin):
        carfax = CarFax(
            vin=vin.vin,
        )
        return CreateCarFax(vin=vin)'''


class Query(graphene.ObjectType):

    ### List ALL objects fields ###
    all_carfax_objects = graphene.List(CarFaxType)
    all_recalls_objects = graphene.List(RecallsType)
    all_adesa_purchases_objects = graphene.List(AdesaPurchasesType)
    all_adesa_runlist_objects = graphene.List(AdesaRunListType)

    ### Retrieve ONE object fields ###
    carfax = graphene.Field(lambda: graphene.List(CarFaxType), vin=graphene.String(), run_date=graphene.String())
    recalls = graphene.Field(lambda: graphene.List(RecallsType), vin=graphene.String(), run_date=graphene.String())
    adesa_purchases = graphene.Field(lambda: graphene.List(AdesaPurchasesType), vin=graphene.String(), run_date=graphene.String())
    adesa_runlist = graphene.Field(lambda: graphene.List(AdesaRunListType), vin=graphene.String(), run_date=graphene.String())

    ### Retrieve ALL objects resolvers (endpoints) ###
    def resolve_all_carfax_objects(self, info, **kwargs):
        return CarFax.objects.all()

    def resolve_all_recalls_objects(self, info, **kwargs):
        return GetRecalls.objects.all()

    def resolve_all_adesa_purchases_objects(self, info, **kwargs):
        return GetAdesaPurchases.objects.all()

    def resolve_all_adesa_runlist_objects(self, info, **kwargs):
        return GetAdesaRunList.objects.all()
    ###

    ### Retrieve ONE objects resolvers (endpoints) ###
    def resolve_carfax(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            all_carfax_objects = CarFax.objects.filter(vin__exact=vin)
            return all_carfax_objects

        if run_date is not None:
            all_carfax_objects = CarFax.objects.filter(run_date__exact=run_date)
            return all_carfax_objects

        return None

    def resolve_recalls(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            all_carfax_objects = GetRecalls.objects.filter(vin__exact=vin)
            return all_carfax_objects

        if run_date is not None:
            all_recalls_objects = GetRecalls.objects.filter(run_date__exact=run_date)
            return all_recalls_objects

        return None

    def resolve_adesa_purchases(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            all_carfax_objects = GetAdesaPurchases.objects.filter(vin__exact=vin)
            return all_carfax_objects

        if run_date is not None:
            all_adesa_purchases_objects = GetAdesaPurchases.objects.filter(run_date__exact=run_date)
            return all_adesa_purchases_objects

        return None

    def resolve_adesa_runlist(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            all_carfax_objects = GetAdesaRunList.objects.filter(vin__exact=vin)
            return all_carfax_objects

        if run_date is not None:
            all_recalls_objects = GetAdesaRunList.objects.filter(run_date__exact=run_date)
            return all_recalls_objects

        return None


class UpdateAdesaRunlist(graphene.Mutation):
    class Arguments:
        lookup_fields = AdesaRunlistInput(required=True)
        lookup_rundate = graphene.Argument(AdesaRunlistInput)

    ok = graphene.Boolean
    runlist = graphene.Field(lambda: AdesaRunListType)


    def mutate(root, info, **input):
        vin = input['lookup_fields']['vin']
        run_date = input['lookup_fields']['run_date']

        if vin and run_date:
            instance = GetAdesaRunList.objects.filter(vin=input['lookup_fields']['vin'], run_date=input['lookup_fields']['run_date']).first()
            try:
                if instance:
                    instance.human_valuation = input["lookup_fields"]["human_valuation"]
                    instance.save()
                    return UpdateAdesaRunlist(runlist=instance)

            except ObjectDoesNotExist as error:
                return error

class UpdateShoppingList(graphene.Mutation):
    class Arguments:
        lookup_fields = ShoppingListInput(required=True)
        lookup_rundate = graphene.Argument(ShoppingListInput)

    ok = graphene.Boolean
    runlist = graphene.Field(lambda: ShoppingListType)


    def mutate(root, info, **input):
        vin = input['lookup_fields']['vin']
        run_date = input['lookup_fields']['run_date']

        if vin and run_date:
            instance = ShoppingList.objects.filter(vin=input['lookup_fields']['vin'], run_date=input['lookup_fields']['run_date']).first()
            try:
                if instance:
                    instance.human_valuation = input["lookup_fields"]["human_valuation"]
                    instance.save()
                    return UpdateShoppingList(runlist=instance)

            except ObjectDoesNotExist as error:
                return error



class CreateCarFax(graphene.Mutation):
    ## https://github.com/graphql-python/graphene/blob/master/UPGRADE-v2.0.md#clientidmutationmutate_and_get_payload
    class Arguments:
        # Arguments attributes are the arguments that the mutation needs for resolving
        #vin = CarFaxInput(required=True)
        carfax_info = CarFaxInput(required=True)

    ok = graphene.Boolean()  # person and ok are output fields when the mutation is resolved
    carfax = graphene.Field(lambda: CarFaxType)


    def mutate(root, info, **input):
        carfax = CarFax(
            vin=input['carfax_info']['vin'],)
        carfax.save()  # this step is necessary

        return CreateCarFax(carfax=carfax)






'''class Mutation(graphene.ObjectType):
    create_carfax = CreateCarFax.Field()'''


'''class CreateCarFax(SerializerMutation):
    class Meta:
        serializer_class = AdesaRunlistSerializer

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        print('here1')
        if 'vin' and 'run_date' in input:
            instance = GetAdesaRunList.objects.filter(vin=input['vin'], run_date=input['run_date']).first()
            if instance:
                # if the instance exists, update it with the sent "humanValuation" value
                return {'instance': instance, 'data': input, 'partial': True}
            else:
                print(input)
                raise ValueError

        return {'data': input, 'partial': True}



    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        print(input)

        kwargs = cls.get_serializer_kwargs(root, info, **input)
        serializer = cls._meta.serializer_class(**kwargs)

        if serializer.is_valid():
            return cls.perform_mutate(serializer, info)
        else:
            'errors = [
                ErrorType(field=key, messages=value)
                for key, value in serializer.errors.items()
            ]

            return cls(errors=errors)
            return 'no'''


class Mutation(graphene.ObjectType):
    create_carfax = CreateCarFax.Field()
    update_runlist = UpdateAdesaRunlist.Field()
    update_shoppinglist = UpdateShoppingList.Field()

class CarFaxUnion(DjangoObjectType):
    class Meta:
        model = CarFax

class RecallsUnion(DjangoObjectType):
    class Meta:
        model = GetRecalls

'''class SearchResult(graphene.Union):

    def resolve_(cls, instance, info):
        class Meta:
            types = (CarFaxUnion, RecallsUnion)'''






schema = graphene.Schema(query=Query, mutation=Mutation)

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