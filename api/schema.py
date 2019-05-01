from graphene_django import DjangoObjectType
import graphene
from api.models import CarFax, GetRecalls, GetAdesaRunList, GetAdesaPurchases
from api.serializers import *
from graphene import ObjectType, Node, Schema, relay
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
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

class AdesaPurchasesInput(graphene.InputObjectType):
    vin = graphene.String(required=True)

class AdesaRunlistInput(graphene.InputObjectType):
    vin = graphene.String(required=True)
    run_date = graphene.String(required=True)

class AdesaRunlistLookUpInput(graphene.InputObjectType):
    vin = graphene.String(required=True)
    run_date = graphene.String(required=True)

class AdesaRunlistUpdateInput(graphene.InputObjectType):
    human_valuation = graphene.String()
    trim = graphene.String()
    check = graphene.String()

class ShoppingListInput(graphene.InputObjectType):
    vin = graphene.String(required=True)
    run_date = graphene.String(required=True)

class ShoppingListUpdateInput(graphene.InputObjectType):
    human_valuation = graphene.String()
    trim = graphene.String()

class ShoppingListDeleteInput(graphene.InputObjectType):
    id = graphene.String(required=True)

class SearchResult(graphene.Union):
    class Meta:
        types = (CarFaxType, RecallsType)

class Query(graphene.ObjectType):

    ### List ALL objects fields ###
    all_carfax_objects = graphene.List(CarFaxType)
    all_recalls_objects = graphene.List(RecallsType)
    all_adesa_purchases_objects = graphene.List(AdesaPurchasesType)
    all_adesa_runlist_objects = graphene.List(AdesaRunListType)
    runlist_paginated = graphene.List(AdesaRunListType, page_no=graphene.Int())
    all_shopping_list_objects = graphene.List(ShoppingListType)



### Retrieve ONE object fields ###
    carfax = graphene.Field(lambda: graphene.List(CarFaxType), vin=graphene.String(), run_date=graphene.String())
    recalls = graphene.Field(lambda: graphene.List(RecallsType), vin=graphene.String(), run_date=graphene.String())
    adesa_purchases = graphene.Field(lambda: graphene.List(AdesaPurchasesType), vin=graphene.String(), run_date=graphene.String())
    adesa_runlist = graphene.Field(lambda: graphene.List(AdesaRunListType), vin=graphene.String(), run_date=graphene.String(), auction_location=graphene.String(), lane=graphene.String())
    shopping_list = graphene.Field(lambda: graphene.List(ShoppingListType), vin=graphene.String(), run_date=graphene.String())
    shopping_list_by_check = graphene.Field(lambda: graphene.List(ShoppingListType), run_date=graphene.String(), check=graphene.String())

    search = graphene.List(SearchResult, q=graphene.String())

    ### Search fields ###
    def resolve_search(self, info, **args):
        q = args.get("q")
        return CarFax.objects.all()

    ### Retrieve ALL objects resolvers (endpoints) ###
    def resolve_all_carfax_objects(self, info, **kwargs):
        return CarFax.objects.all()

    def resolve_all_recalls_objects(self, info, **kwargs):
        return GetRecalls.objects.all()
    def resolve_all_adesa_purchases_objects(self, info, **kwargs):
        return GetAdesaPurchases.objects.all()

    def resolve_runlist_paginated(self, info, **kwargs):
        objects = GetAdesaRunList.objects.all()

        page_no = kwargs.get('page_no')
        p = Paginator(objects, 2)
        current_page = p.page(page_no)

        return current_page

    def resolve_all_adesa_runlist_objects(self, info, **kwargs):
        return GetAdesaRunList.objects.all()

    def resolve_all_shopping_list_objects(self, info, **kwargs):
        return ShoppingList.objects.all()

    ### Retrieve ONE object resolvers (endpoints) ###
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
            all_recalls_objects = GetRecalls.objects.filter(vin__exact=vin)
            return all_recalls_objects

        if run_date is not None:
            all_recalls_objects = GetRecalls.objects.filter(run_date__exact=run_date)
            return all_recalls_objects

        return None

    def resolve_adesa_purchases(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            all_adesa_purchases_objects = GetAdesaPurchases.objects.filter(vin__exact=vin)
            return all_adesa_purchases_objects

        if run_date is not None:
            all_adesa_purchases_objects = GetAdesaPurchases.objects.filter(run_date__exact=run_date)
            return all_adesa_purchases_objects

        return None

    def resolve_adesa_runlist(self, info, **kwargs):
        vin = kwargs.get('vin')
        auction_location = kwargs.get('auction_location')
        run_date = kwargs.get('run_date')
        lane = kwargs.get('lane')

        print(lane)
        if vin is not None:
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(vin__exact=vin)
            return all_adesa_runlist_objects

        if run_date is not None and auction_location is None and lane is None:  # if auction_location is only supplied
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(run_date__exact=run_date)
            return all_adesa_runlist_objects

        if auction_location is not None and run_date is None and lane is None:  # if auction_location is only supplied
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(auction_location__exact=auction_location).order_by('run_date').distinct('run_date')
            return all_adesa_runlist_objects

        if lane is not None and auction_location is None and run_date is None:  # if lane is only supplied
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(lane__exact=lane)
            return all_adesa_runlist_objects

        if auction_location is not None and run_date is not None and lane is None:  # if auction_location and run_date are only supplied
            print("hereee")
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(auction_location__exact=auction_location, run_date__exact=run_date).order_by('lane').distinct('lane')
            return all_adesa_runlist_objects

        if auction_location is not None and run_date is not None and lane is not None:  # if all three are supplied
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(run_date__exact=run_date, auction_location__exact=auction_location, lane__exact=lane)
            return all_adesa_runlist_objects

        if lane is not None and auction_location is None and run_date is None:  # if lane is only supplied
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(lane__exact=lane)
            return all_adesa_runlist_objects

        if lane is not None:
            all_adesa_runlist_objects = GetAdesaRunList.objects.filter(lane__exact=lane)
            return all_adesa_runlist_objects

        return None

    def resolve_shopping_list(self, info, **kwargs):
        vin = kwargs.get('vin')
        run_date = kwargs.get('run_date')

        if vin is not None:
            all_shopping_list_objects = ShoppingList.objects.filter(vin__exact=vin)
            return all_shopping_list_objects

        if run_date is not None:
            all_shopping_list_objects = ShoppingList.objects.filter(run_date__exact=run_date)
            return all_shopping_list_objects

        return None

    def resolve_shopping_list_by_check(self, info, **kwargs):
        run_date = kwargs.get('run_date')
        check = kwargs.get('check')

        if run_date and check:
            instance = ShoppingList.objects.filter(run_date__exact=run_date, check__exact=check)
            if instance:
                return instance

        return None


class CreateCarFax(graphene.Mutation):
    ## https://github.com/graphql-python/graphene/blob/master/UPGRADE-v2.0.md#clientidmutationmutate_and_get_payload
    class Arguments:
        # Arguments attributes are the arguments that the mutation needs for resolving
        #vin = CarFaxInput(required=True)
        carfax_info = graphene.Argument(CarFaxInput)

    ok = graphene.Boolean()  # carfax and ok are output fields when the mutation is resolved
    carfax = graphene.Field(lambda: CarFaxType)


    def mutate(root, info, **input):
        carfax = CarFax(
            vin=input['carfax_info']['vin'],)
        carfax.save()  # this step is necessary

        return CreateCarFax(carfax=carfax)


class CreateAdesaRunlist(graphene.Mutation):
    class Arguments:
        runlist_info = graphene.Argument(AdesaRunlistInput)

    ok = graphene.Boolean()
    runlist = graphene.Field(lambda: AdesaRunListType)

    def mutate(root, info, **input):
        runlist = GetAdesaRunList(
            vin=input['runlist_info']['vin'],)
        runlist.save()  # this step is necessary

        return CreateAdesaRunlist(runlist=runlist)

class DeleteShoppingListById(graphene.Mutation):
    class Arguments:
        record = graphene.Argument(ShoppingListDeleteInput)

    ok = graphene.Boolean()
    # shoppingList = graphene.Field(lambda: ShoppingListType)

    def mutate(self, info, **input):
        instance = ShoppingList.objects.get(id=input['record']['id'])

        if instance:
            instance.delete()

        return DeleteShoppingListById(ok=True)


class CreateShoppinglist(graphene.Mutation):
    class Arguments:
        list_info = graphene.Argument(ShoppingListInput)

    ok = graphene.Boolean()
    response = graphene.String()
    list = graphene.Field(lambda: ShoppingListType)

    def mutate(root, info, **input):
        # attempt to retrieve the record first
        instance = ShoppingList.objects.filter(vin=input['list_info']['vin'], run_date=input['list_info']['run_date']).first()

        if instance:
            return CreateAdesaRunlist(response="That car is already on the Shopping List")

        else:
            list = ShoppingList(vin=input['list_info']['vin'], run_date=input['list_info']['run_date'])
            list.save()
            return CreateShoppinglist(list=list)

class CreateAdesaPurchase(graphene.Mutation):
    class Arguments:
        purchase_info = AdesaPurchasesInput(required=True)

    ok = graphene.Boolean()
    purchase = graphene.Field(lambda: AdesaRunListType)

    def mutate(root, info, **input):
        purchase = GetAdesaPurchases(vin=input['purchase_info']['vin'],)
        purchase.save()

        return CreateAdesaPurchase(purchase=purchase)

class UpdateAdesaRunlist(graphene.Mutation):

    class Arguments:
        lookup_fields = AdesaRunlistLookUpInput()
        fields_to_update = AdesaRunlistUpdateInput()  # only need trim and human_valuation

    ok = graphene.Boolean()
    runlist = graphene.Field(lambda: AdesaRunListType)

    def mutate(root, info, **input):
        update_keys = list(input["fields_to_update"].keys())
        vin = input['lookup_fields']['vin']
        run_date = input['lookup_fields']['run_date']

        human_valuation = None
        trim = None
        check = None

        if "human_valuation" in update_keys:
            human_valuation = input["fields_to_update"]["human_valuation"]

        if 'trim' in update_keys:
            trim = input["fields_to_update"]["trim"]

        if 'check' in update_keys:
            check = input["fields_to_update"]["check"]

        if vin and run_date:
            instance = GetAdesaRunList.objects.filter(vin=input['lookup_fields']['vin'], run_date=input['lookup_fields']['run_date']).first()
            try:
                if instance:
                    if human_valuation:
                        instance.human_valuation = human_valuation
                    if trim:
                        instance.trim = trim
                    if check:
                        instance.check = check
                    instance.save()
                    return UpdateAdesaRunlist(ok=True, runlist=instance)

            except ObjectDoesNotExist as error:
                return error

class UpdateShoppingList(graphene.Mutation):
    class Arguments:
        lookup_fields = ShoppingListInput()
        fields_to_update = ShoppingListUpdateInput()  # only need trim and human_valuation

    ok = graphene.Boolean()
    runlist = graphene.Field(lambda: ShoppingListType)

    def mutate(root, info, **input):
        update_keys = list(input["fields_to_update"].keys())
        vin = input['lookup_fields']['vin']
        run_date = input['lookup_fields']['run_date']

        human_valuation = None
        trim = None

        if "human_valuation" in update_keys:
            human_valuation = input["fields_to_update"]["human_valuation"]

        if 'trim' in update_keys:
            trim = input["fields_to_update"]["trim"]

        if vin and run_date:
            instance = ShoppingList.objects.filter(vin=input['lookup_fields']['vin'], run_date=input['lookup_fields']['run_date']).first()
            try:
                if instance:
                    if human_valuation:
                        instance.human_valuation = human_valuation
                    if trim:
                        instance.trim = trim
                    instance.save()
                    return UpdateShoppingList(runlist=instance)

            except ObjectDoesNotExist as error:
                return error

class DeleteShoppingList(graphene.Mutation):

    class Arguments:
        lookup_fields = ShoppingListInput()

    ok = graphene.Boolean()
    response = graphene.String()
    deleted_field = graphene.Field(lambda: ShoppingListType)

    def mutate(root, info, **input):
        vin = input['lookup_fields']['vin']
        run_date = input['lookup_fields']['run_date']
        if vin and run_date:
            instance = ShoppingList.objects.filter(vin=input['lookup_fields']['vin'], run_date=input['lookup_fields']['run_date']).first()
            try:
                if instance:
                    instance.delete()
                    return DeleteShoppingList(response="Record with VIN: %s has been deleted" % vin)
                else:
                    return DeleteShoppingList(response="That record does not exist")
            except ObjectDoesNotExist:
                return DeleteShoppingList(ok=False)


class Mutation(graphene.ObjectType):
    create_carfax = CreateCarFax.Field()
    create_runlist = CreateAdesaRunlist.Field()
    create_shopping_list = CreateShoppinglist.Field()
    create_adesa_purchase = CreateAdesaPurchase.Field()
    update_runlist = UpdateAdesaRunlist.Field()
    update_shoppinglist = UpdateShoppingList.Field()
    delete_shoppinglist = DeleteShoppingList.Field()
    delete_shoppinglist_by_id = DeleteShoppingListById.Field()




'''class CarFaxUnion(DjangoObjectType):
    class Meta:
        model = CarFax

class RecallsUnion(DjangoObjectType):
    class Meta:
        model = GetRecalls'''


schema = graphene.Schema(query=Query, mutation=Mutation, types=[CarFaxType, RecallsType, SearchResult])