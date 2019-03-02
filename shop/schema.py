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
class SpecificationType(DjangoObjectType):
    class Meta:
        model = models.Specification
class AddressOneType(DjangoObjectType):
    class Meta:
        model = models.AddressOne

class AddressTwoType(DjangoObjectType):
    class Meta:
        model = models.AddressTwo

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
class WishlistType(DjangoObjectType):
    class Meta:
        model = models.Wishlist

class Query(graphene.AbstractType):
    all_device= graphene.List(DeviceType)
    all_component= graphene.List(ComponentType)
    all_cart= graphene.List(CartType) 
    all_order= graphene.List(OrderType)
    all_banner=graphene.List(BannerType)
    all_wishlist=graphene.List(WishlistType)
    specification = graphene.Field(SpecificationType)
    me = graphene.Field(CustomUserType)
    wishlist = graphene.Field(WishlistType)
    all_specification = graphene.List(SpecificationType)
    device = graphene.Field(DeviceType,id=graphene.Int())
    cart = graphene.Field(CartType,id=graphene.Int())
    order = graphene.Field(OrderType,id=graphene.Int())
    component = graphene.Field(ComponentType,id=graphene.Int())
    manufacturer = graphene.List(DeviceType,id=graphene.Int())
    address_one = graphene.Field(AddressOneType)
    address_two = graphene.Field(AddressTwoType)
    
    def resolve_address_one(self,info,**kwargs):
        user = info.context.user
        address_one = user.address_one
        return address_one

    def resolve_address_two(self,info,**kwargs):
        user = info.context.user
        address_two= user.address_two
        return address_two

    def resolve_all_wishlist(self,info,**kwargs):
        return models.Wishlist.objects.all() 
    def resolve_all_device(self,info,**kwargs):
        return models.Device.objects.all()
    def resolve_all_banner(self,info,**kwargs):
        return models.Banner.objects.all()
    def resolve_all_specification(self,info,**kwargs):
        return models.Specification.objects.all() 
    def resolve_all_component(self,info,**kwargs):
        return models.Component.objects.all()
    def resolve_all_cart(self,info,**kwargs):
        return models.Cart.objects.all()
    def resolve_device(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Device.objects.get(id=id)
    def resolve_wishlist(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Wishlist.objects.get(id=id)


    def resolve_component(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Component.objects.get(id=id)
    def resolve_specification(self,info,**kwargs):
        id = kwargs.get('id')
        return models.Specification.objects.get(id=id)

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
    specification = graphene.Field(SpecificationType) 
    class Arguments:
        name=graphene.String()
        version = graphene.String()
        hw_specification = graphene.String()
        sw_specification = graphene.String()
        support_notes = graphene.String()
    def mutate(self,info,name,version,hw_specification,sw_specification):
        component=models.Component(name=name)
        component.save()
        specification = models.Specification.objects.create(version=version,hw_specification=hw_specification,
        sw_specification=sw_specification)
        component.specification = specification
        component.save()
        return CreateComponent(
            id=component.id,
            name=component.name,
            specification = component.specification,
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
class CreateCustomUser(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)

    class Arguments:
        firstname=graphene.String(required=True)
        lastname=graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        usertype = graphene.String(required=True)
        
    def mutate(self,info,username,password,email,usertype,firstname,lastname):
        customuser = models.CustomUser(username=username,email=email,usertype=usertype,first_name=firstname,last_name=lastname)
        customuser.save()
        customuser.set_password(password)
        customuser.name = customuser.first_name+" "+customuser.last_name
        customuser.save()
        return CreateCustomUser(customuser)
class ProfileUpdate(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)

    class Arguments:
        username= graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        usertype = graphene.String()
        address_one = graphene.Int()
        address_two = graphene.Int()

    def mutate(self,info,**kwargs):
        customuser = info.context.user
        if kwargs.get('username') is not None:
            customuser.username = kwargs.get('username')
        if kwargs.get('first_name') is not None:
            customuser.first_name = kwargs.get('first_name')
        if kwargs.get('last_name') is not None:
            customuser.last_name  = kwargs.get('last_name')
        if kwargs.get('email') is not None:
            customuser.email= kwargs.get('email')
        if kwargs.get('usertype') is not None:
            customuser.usertype= kwargs.get('usertype')
        if kwargs.get('address_one') is not None:
            address_one = kwargs.get('address_one')
            address_one = models.AddressOne.get(id=address_one)
            customuser.address_one= address_one
        if kwargs.get('address_two') is not None:
            address_two= kwargs.get('address_two')
            address_two= models.AddressOne.get(id=address_two)
            customuser.address_two= address_two
        customuser.save()
        return CreateCustomUser(customuser)

class AddressOneUpdate(graphene.Mutation):
    address_one = graphene.Field(AddressOneType)

    class Arguments:
        name = graphene.String()
        phone_number = graphene.Int()
        pincode = graphene.Int()
        locality = graphene.String()
        address = graphene.String() 
        city_district_town =  graphene.String()
        state = graphene.String()
        landmark = graphene.String()
        address_type = graphene.String()

    def mutate(self,info,**kwargs):
        customuser = info.context.user
        if kwargs.get('username') is not None:
            customuser.username = kwargs.get('username')
        if kwargs.get('first_name') is not None:
            customuser.first_name = kwargs.get('first_name')
        if kwargs.get('last_name') is not None:
            customuser.last_name  = kwargs.get('last_name')
        if kwargs.get('email') is not None:
            customuser.email= kwargs.get('email')
        if kwargs.get('usertype') is not None:
            customuser.usertype= kwargs.get('usertype')
        if kwargs.get('address_one') is not None:
            address_one = kwargs.get('address_one')
            address_one = models.AddressOne.get(id=address_one)
            customuser.address_one= address_one
        if kwargs.get('address_two') is not None:
            address_two= kwargs.get('address_two')
            address_two= models.AddressOne.get(id=address_two)
            customuser.address_two= address_two
        customuser.save()
        return CreateCustomUser(customuser)



class CreateAddressOne(graphene.Mutation):

    address_one= graphene.Field(AddressOneType)

    class Arguments:
        name = graphene.String(required=True)
        phone_number = graphene.Int(required=True)
        pincode = graphene.Int(required=True)
        locality = graphene.String(required=True)
        address = graphene.String() 
        city_district_town =  graphene.String()
        state = graphene.String()
        landmark = graphene.String()
        address_type = graphene.String()

    def mutate(self,info,name,phone_number,pincode,locality,address,city_district_town,state,landmark,address_type):
        user = info.context.user 
        address_one = models.AddressOne(name=name,
        phone_number=phone_number,
        pincode=pincode,
        locality=locality,
        address=address,
        city_district_town=city_district_town,
        state=state,
        landmark=landmark,
        address_type=address_type)
        address_one.save()
        user.address_one =address_one
        user.save()
        return CreateAddressOne(customuser)

class CreateAddressTwo(graphene.Mutation):

    address_two= graphene.Field(AddressTwoType)

    class Arguments:
        name = graphene.String(required=True)
        phone_number = graphene.Int(required=True)
        pincode = graphene.Int(required=True)
        locality = graphene.String(required=True)
        address = graphene.String() 
        city_district_town =  graphene.String()
        state = graphene.String()
        landmark = graphene.String()
        address_type = graphene.String()

    def mutate(self,info,name,phone_number,pincode,locality,address,city_district_town,state,landmark,address_type):
        user = info.context.user 
        address_two= models.AddressTwo(name=name,
        phone_number=phone_number,
        pincode=pincode,
        locality=locality,
        address=address,
        city_district_town=city_district_town,
        state=state,
        landmark=landmark,
        address_type=address_type)
        address_two.save()
        user.address_two = address_two
        user.save()
        return CreateAddressTwo(address_two)



#Types
class SpecificationInput(graphene.InputObjectType):
    id = graphene.Int()
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

class CreateDevice(graphene.Mutation):
    id = graphene.Int()
    name=graphene.String()
    manufacturer = graphene.Field(CustomUserType)
    model_number = graphene.Int()
    version = graphene.String(required=True)
    hw_specification = graphene.String(required=True)
    sw_specification = graphene.String(required=True)
    support_notes = graphene.String(required=True)


    class Arguments:
        name=graphene.String()
        model_number=graphene.Int()
        version = graphene.String(required=True)
        hw_specification = graphene.String(required=True)
        sw_specification = graphene.String(required=True)
        support_notes = graphene.String(required=True)

    def mutate(self,info,name,model_number,version,hw_specification,sw_specification,support_notes):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
        
        device = models.Device(name=name,manufacturer=current_user,model_number=model_number)
        device.save()
        specification = models.Specification.objects.create(version=version,hw_specification=hw_specification,sw_specification=sw_specification)
        device.specification = specification
        device.save()

        return CreateDevice(
            id=device.id,
            name=device.name,
            manufacturer=current_user,
            version = device.specification.version,
            hw_specification = device.specification.hw_specification,
            sw_specification = device.specification.sw_specification,
            support_notes = device.specification.support_notes,
        )

class AddComponent(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)
    device = graphene.Field(DeviceType)
    component = graphene.Field(ComponentType)
    class Arguments:
        device_id = graphene.Int(required=True)
        component_id = graphene.Int(required=True) 

    def mutate(self,info,device_id,component_id):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
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
        device_id = graphene.Int(required=True)
    def mutate(self,info,username,device_id):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
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
        id = graphene.Int(required=True)
    def mutate(self,info,id):
        buyer= info.context.user
        banner = models.Banner.objects.get(id=id)
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
        id = graphene.Int(required=True)
    def mutate(self,info,id):
        buyer = info.context.user
        banner = models.Banner.objects.get(id=id)
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
        banner = graphene.Int(required=True)
    def mutate(self,info,id):
        buyer= info.context.user
        cart = models.Cart.objects.get(buyer=buyer)
        banner = cart.banners.get(id=id) 
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
        id = graphene.Int(required=True)
        price = graphene.Int(required=True)
    def mutate(self,info,id,price):
        seller = info.context.user 
        device = models.Device.objects.get(id=id)
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
    document =  Upload(required=True)

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        document =  Upload(required=True)
    
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
    profie_update = ProfileUpdate.Field()
    create_address_one = CreateAddressOne.Field()
    create_address_two = CreateAddressTwo.Field()