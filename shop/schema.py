import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene_django.types import DjangoObjectType
from django.contrib.postgres.search import TrigramSimilarity
from . import models
from graphene_file_upload.scalars import Upload
class BannerType(DjangoObjectType):
    class Meta:
        model = models.Banner
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
    all_banner=graphene.List(BannerType)
    me = graphene.Field(CustomUserType)

    device = graphene.Field(DeviceType,id=graphene.Int())
    cart = graphene.Field(CartType,id=graphene.Int())
    order = graphene.Field(OrderType,id=graphene.Int())
    component = graphene.Field(ComponentType,id=graphene.Int())
    manufacturer = graphene.List(DeviceType,id=graphene.Int())
    
    def resolve_all_device(self,info,**kwargs):
        return models.Device.objects.all()
    def resolve_all_banner(self,info,**kwargs):
        return models.Banner.objects.all()
    
    def resolve_all_component(self,info,**kwargs):
        return models.Component.objects.all()
    def resolve_all_cart(self,info,**kwargs):
        return models.Cart.objects.all()
    def resolve_device(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Device.objects.get(id=id)
    def resolve_all_order(self,info,**kwargs):
        return models.Order.objects.all()
    def resolve_component(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Component.objects.get(id=id)
    def resolve_manufacturer(self,info,**kwargs):
        id = kwargs.get('id')
        manufacturer = models.CustomUser.objects.get(id=id)
        devices = models.Device.objects.all().filter(manufacturer=manufacturer)
        return devices
    def resolve_cart(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Cart.objects.get(id=id)
    
    def resolve_order(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Order.objects.get(id=id)

    def resolve_order(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Banner.objects.get(id=id)


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
class DeviceSearch(graphene.Mutation):
    devices = graphene.List(DeviceType)

    class Arguments:
        query = graphene.String(required=True)

    def mutate(self,info,query):
        results = models.Device.objects.annotate(
        similarity=TrigramSimilarity('name',query),
        ).filter(similarity__gt=0.0).order_by('-similarity')
        print(results)
        return DeviceSearch(
            devices = results
        )
class CreateDevice(graphene.Mutation):
    id = graphene.Int()
    name=graphene.String()
    manufacturer = graphene.Field(CustomUserType)
    model_number = graphene.Int()
    class Arguments:
        name=graphene.String()
        model_number=graphene.Int()
    def mutate(self,info,name,model_number):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
        
        device = models.Device(name=name,manufacturer=current_user,model_number=model_number)
        device.save()
        return CreateDevice(
            id=device.id,
            name=device.name,
            manufacturer=current_user
        )
class CreateCustomUser(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)

    class Arguments:
        firstname=graphene.String(required=True)
        lastname=graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        usertype = graphene.String(required=True)
        
    def mutate(self,info,username,password,email,usertype):
        customuser = models.CustomUser(username=username,password=password,email=email,usertype=usertype,first_name=firstname,last_name=lastname)
        customuser.save()
        return CreateCustomUser(customuser)


#InputTypes
class DeviceInput(graphene.InputObjectType):
    id = graphene.Int()
class CustomUserInput(graphene.InputObjectType):
    username = graphene.String()
class ComponentInput(graphene.InputObjectType):
    id = graphene.Int()
class BannerInput(graphene.InputObjectType):
    id = graphene.Int()
class OrderInput(graphene.InputObjectType):
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
class AddDeviceSeller(graphene.Mutation):
    sellers = graphene.List(CustomUserType)
    device = graphene.Field(DeviceType)
    class Arguments:
        username = graphene.String(required=True)
        device = DeviceInput(required=True)
    def mutate(self,info,username,device):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
        if current_user.username != username :
            raise Exception("Not a Valid User!!")
        if device is not None:
            device_id = device.id
            device = models.Device.objects.get(id=device_id)
            user = models.CustomUser.objects.get(username=username)
            if device.manufacturer.username == current_user.username :
               device.sellers.add(user)
               device.save()
               sellers = device.sellers.all()
        return  AddDeviceSeller(
            sellers = sellers,
            device = device,
        )
class AddBannerCart(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    banners = graphene.List(BannerType)
    class Arguments:
        buyer= CustomUserInput(required=True)
        banner = BannerInput(required=True)
    def mutate(self,info,buyer,banner):
        buyer= models.CustomUser.objects.get(username=buyer.username)
        banner = models.Banner.objects.get(id=banner.id)
        try :
            cart = models.Cart.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            cart = models.Cart.objects.create(buyer=buyer)
        cart.banners.add(banner)
        cart.save()
        banners=cart.banners.all()
        return  AddBannerCart(
            buyer=buyer,
            banners=banners
        )
class AddBannerWishlist(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    banners = graphene.List(BannerType)
    class Arguments:
        buyer= CustomUserInput(required=True)
        banner = BannerInput(required=True)
    def mutate(self,info,buyer,banner):
        buyer= models.CustomUser.objects.get(username=buyer.username)
        banner = models.Banner.objects.get(id=banner.id)
        try :
            wishlist= models.Wishlist.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            wishlist = models.Wishlist.objects.create(buyer=buyer)
        wishlist.banners.add(banner)
        wishlist.save()
        banners=wishlist.banners.all()
        return  AddBannerWishlist(
            buyer=buyer,
            banners=banners
        )

class MoveBannerWishlist(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    banners = graphene.List(BannerType)
    class Arguments:
        buyer= CustomUserInput(required=True)
        banner = BannerInput(required=True)
    def mutate(self,info,buyer,banner):
        buyer= models.CustomUser.objects.get(username=buyer.username)
        cart = models.Cart.objects.get(buyer=buyer)
        banner = cart.banners.get(id=banner.id) 
        try :
            wishlist= models.Wishlist.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            wishlist = models.Wishlist.objects.create(buyer=buyer)
        wishlist.banners.add(banner)
        wishlist.save()
        cart.banners.remove(banner)
        cart.save()
        banners=wishlist.banners.all()
        return  MoveBannerWishlist(
            buyer=buyer,
            banners = banners
        )

class CreateOrder(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    banners = graphene.List(BannerType)
    approval = graphene.Boolean()
    class Arguments:
        buyer= CustomUserInput(required=True)
    def mutate(self,info,buyer):
        buyer= models.CustomUser.objects.get(username=buyer.username)
        order = models.Order.objects.create(buyer=buyer)
        cart = models.Cart.objects.get(buyer=buyer)
        banners = cart.banners.all()
        for banner in banners:
            order.banners.add(banner)
            order.save()
        cart.save()
        banners=cart.banners.all()
        return  CreateOrder(
            buyer=buyer,
            banners=banners,
            approval = order.approval
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

class CreateBanner(graphene.Mutation):
    seller = graphene.Field(CustomUserType)
    banner = graphene.Field(BannerType)
    class Arguments:
        seller = CustomUserInput(required=True) 
        device = DeviceInput(required=True)
        price = graphene.Int(required=True)
    def mutate(self,info,seller,device,price):
        device = models.Device.objects.get(id=device.id)
        seller = models.CustomUser.objects.get(username=seller.username)
        if not device.sellers.all().filter(id=seller.id).exists():
            raise Exception("Seller is not and Authorized device seller")
        banner = models.Banner(seller =seller,device=device,price=price)
        banner.save()
        return CreateBanner(
            seller=seller,banner = banner
        )


class ApproveOrder(graphene.Mutation):
    order = graphene.Field(OrderType)
    approval= graphene.Boolean()
    class Arguments:
        order =  OrderInput(required=True)
    def mutate(self,info,order):
        order = models.Order.objects.get(id=order.id)
        order.approval = True
        order.save()
        cart = models.Cart.objects.get(buyer=order.buyer)

        banners  = order.banners.all()
        for banner in banners:
            cart.banners.remove(banner)
            cart.save()
        return ApproveOrder(
            order=order,approval=order.approval
        )

class FileUpload(graphene.Mutation):
    name = graphene.String()
    description = graphene.String()
    document =  Upload()

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        document =  Upload()
    
    def mutate(self,info,file,**kwargs):
        name = kwargs.get('name')
        description = kwargs.get('description')
        document = info.context.FILES.get(file)

        newfile = models.File(
            name = name,
            description = description,
            document = document,
        ) 

        newfile.save()

        return FileUpload(
            name = newfile.name,
            description = newfile.description,
            document = newfile.document,
        )



class Mutation(graphene.ObjectType):
    create_component = CreateComponent.Field()
    create_device = CreateDevice.Field()
    create_customuser=CreateCustomUser.Field() 
    change_password = ChangePassword.Field()   
    add_component = AddComponent.Field()
    add_device_seller = AddDeviceSeller.Field()
    create_banner = CreateBanner.Field()
    add_banner_cart = AddBannerCart.Field()
    move_banner_wishlist = MoveBannerWishlist.Field()
    create_order = CreateOrder.Field()
    approve_order = ApproveOrder.Field()
    add_banner_wishlist=AddBannerWishlist.Field()
    device_search = DeviceSearch.Field()    
    file_upload = FileUpload.Field()