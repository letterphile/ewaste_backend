import graphene

from graphene_django.types import DjangoObjectType

from . import models

class DeviceType(DjangoObjectType):
    class Meta:
        model = models.Device

class ComponentType(DjangoObjectType):
    class Meta:
        model = models.Component

class CustomUserType(DjangoObjectType):
    class Meta:
        model = models.CustomUser

class OrderType(DjangoObjectType):
    class Meta:
        model = models.Order

class CartType(DjangoObjectType):
    class Meta:
        model = models.Cart

class Query(graphene.AbstractType):
    all_device= graphene.List(DeviceType)
    all_component= graphene.List(ComponentType)
    all_cart= graphene.List(CartType) 
    all_order= graphene.List(OrderType)

    device = graphene.Field(DeviceType,id=graphene.Int())
    cart = graphene.Field(CartType,id=graphene.Int())
    order = graphene.Field(OrderType,id=graphene.Int())
    component = graphene.Field(ComponentType,id=graphene.Int())

    def resolve_all_device(self,info,**kwargs):
        print("args: "+str(args))
        return models.Device.objects.all()

    def resolve_all_component(self,info,**kwargs):
        print("args: "+str(args))
        return models.Component.objects.all()

    def resolve_device(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Device.objects.get(id=id)

    def resolve_component(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Component.objects.get(id=id)

    def resolve_cart(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Cart.objects.get(id=id)
    
    def resolve_order(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Order.objects.get(id=id)

class CreateComponent(graphene.Mutation):
    id = graphene.Int()
    name= graphene.String()
    specs = graphene.String()

    class Arguments:
        name=graphene.String()
        specs = graphene.String()

    def mutate(self,info,name,specs):
        component=models.Component(name=name,specs=specs)
        component.save()
        return CreateComponent(
            id=component.id,
            name=component.name,
            specs=component.specs
        )

class CreateDevice(graphene.Mutation):
    id = graphene.Int()
    name=graphene.String()
    components_id = graphene.List(graphene.Int)
    class Arguments:
        name=graphene.String()
        components_id = graphene.List(graphene.Int)
    def mutate(self,info,name,components_id):
        device = models.Device(name=name)
        device.save()
        for component_id in components_id:
            device.components.add(models.Component.objects.get(id=component_id))
            device.save()
        return CreateDevice(
            id=device.id,
            name=device.name,
            components_id=components_id
        )
class CreateCustomUser(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        usertype = graphene.String(required=True)
        
    def mutate(self,info,username,password,email,usertype):
        customuser = models.CustomUser(username=username,password=password,email=email,usertype=usertype)
        customuser.save()
        return CreateCustomUser(customuser)

class Mutation(graphene.ObjectType):
    create_component = CreateComponent.Field()
    create_device = CreateDevice.Field()
    create_customuser=CreateCustomUser.Field()    