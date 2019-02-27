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

    me = graphene.Field(CustomUserType)

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


    def resolve_me(self,info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not Logged in")
        return user

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
    manufacturer = graphene.Field(CustomUserType)
    price = graphene.Int()
    model_number = graphene.Int()
    class Arguments:
        name=graphene.String()
        price=graphene.Int()
        model_number=graphene.Int()
    def mutate(self,info,name,price,model_number):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
        
        device = models.Device(name=name,manufacturer=current_user,price=price,model_number=model_number)
        device.save()
        return CreateDevice(
            id=device.id,
            name=device.name,
            manufacturer=current_user
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

class DeviceInput(graphene.InputObjectType):
    id = graphene.Int()

class ComponentInput(graphene.InputObjectType):
    id = graphene.Int()

class AddComponent(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)
    device = graphene.Field(DeviceType)
    component = graphene.Field(ComponentType)
    class Arguments:
        username = graphene.String(required=True)
        device = DeviceInput(required=True)
        component = ComponentInput(required=True) 

    def mutate(self,info,username,device,component):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
        if current_user.username != username :
            raise Exception("Not a Valid User!!")
        if device is not None and component is not None:
            device_id = device.id
            component_id = component.id
            device = models.Device.objects.get(id=device_id)
            component = models.Component.objects.get(id=component_id)
            if device.manufacturer.username == current_user.username :
               device.components.add(component) 
               device.save()
        
        return  AddComponent(
            customuser=current_user,
            device = device,
            component=component
        )

class ChangePassword(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)
    
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self,info,username,password):
        current_user = info.context.user 
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
        if current_user.username != username :
            raise Exception("Not a Valid User!!")
        customuser = models.CustomUser.objects.get(username=username)
        customuser.set_password(password)
        customuser.save()

        return ChangePassword(customuser) 
class Mutation(graphene.ObjectType):
    create_component = CreateComponent.Field()
    create_device = CreateDevice.Field()
    create_customuser=CreateCustomUser.Field() 
    change_password = ChangePassword.Field()   
    add_component = AddComponent.Field()