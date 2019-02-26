import graphene

from graphene_django.types import DjangoObjectType

from . import models


class DeviceType(DjangoObjectType):
    class Meta:
        model = models.Device

class ComponentType(DjangoObjectType):
    class Meta:
        model = models.Component

class Query(graphene.AbstractType):
    all_device= graphene.List(DeviceType)
    all_component= graphene.List(ComponentType) 
    
    device = graphene.Field(DeviceType,id=graphene.Int())

    def resolve_all_device(self,args):
        print("args: "+str(args))
        return models.Device.objects.all()

    def resolve_all_component(self,args):
        print("args: "+str(args))
        return models.Component.objects.all()

    def resolve_device(self,args,id):
        return models.Device.objects.get(id=id)

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
class Mutation(graphene.ObjectType):
    create_component = CreateComponent.Field()
    create_device = CreateDevice.Field()