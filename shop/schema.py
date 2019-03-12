import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene_django.types import DjangoObjectType
from . import models
from django.contrib.postgres.search import SearchVector,SearchQuery
class ManufacturerType(DjangoObjectType):
    class Meta:
        model = models.Manufacturer
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
    all_customuser  = graphene.List(CustomUserType)
    all_manufacturer = graphene.List(ManufacturerType) 
    specification = graphene.Field(SpecificationType)
    my_address = graphene.Field(AddressOneType)
    me = graphene.Field(CustomUserType)
    manufacturedbyme= graphene.List(DeviceType)
    wishlist = graphene.Field(WishlistType)
    all_specification = graphene.List(SpecificationType)
    device = graphene.Field(DeviceType,id=graphene.Int())
    cart = graphene.Field(CartType,id=graphene.Int())
    order = graphene.Field(OrderType,id=graphene.Int())
    component = graphene.Field(ComponentType,id=graphene.Int())
    my_devices= graphene.List(DeviceType)
    my_components = graphene.List(ComponentType) 
    address_one = graphene.Field(AddressOneType)
    address_two = graphene.Field(AddressTwoType)
    rahul_add = graphene.String()
    def resolve_rahul_add(self,info,**kwargs):
        user = info.context.user
        address = user.address_one
        string_address = address.address
        return (string_address) 
    def resolve_my_address(self,info,**kwargs):
        user = info.context.user
        address = user.address
        return address 
    def resolve_my_devices(self,info,**kwargs):
        user = info.context.user
        devices = user.device_set.all()
        return devices
    
    def resolve_my_components(self,info,**kwargs):
        user = info.context.user
        components = user.component_set.all()

        return  components

    
    def resolve_address_one(self,info,**kwargs):
        user = info.context.user
        address_one = user.address_one
        return address_one
    def resolve_all_customuser(self,info,**kwargs):
        return  models.CustomUser.objects.all()
    def resolve_manufactured_by_me(self,info,**kwargs):
        user = info.context.user
        devices = models.Device.objects.filter(manufacturer=user)
        return devices

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

    def resolve_all_manufacturer(self,info,**kwargs):
        return models.Manufacturer.objects.all()


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

    def resolve_me(self,info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not Logged in")
        return user

class UpdateDevice(graphene.Mutation):
    id = graphene.Int()
    name= graphene.String()
    specification = graphene.Field(SpecificationType) 
    class Arguments:
        id  = graphene.Int()
        name=graphene.String()
        version = graphene.String()
        hw_specification = graphene.String()
        sw_specification = graphene.String()
        support_notes = graphene.String()
        manufacturer_name = graphene.String() 
    def mutate(self,info,id,**kwargs):
        device = models.Device.objects.get(id=id)
        specification = device.specification 
        if kwargs.get('name') is not None :
           device.name = kwargs.get('name')
        if kwargs.get('version') is not None :
           specification.version= kwargs.get('version')
        if kwargs.get('hw_specification') is not None :
           specification.hw_specification= kwargs.get('hw_specification')
        if kwargs.get('sw_specification') is not None :
           specification.sw_specification= kwargs.get('sw_specification')
        if kwargs.get('support') is not None :
           specification.support= kwargs.get('support')
        device= device.save()
        specification =specification.save()        

        return UpdateDevice(
            id=device.id,
            name=device.name,
            specification = device.specification,
        )

class DeleteDevice(graphene.Mutation):
    id = graphene.Int()
    name= graphene.String()
    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self,info,id,**kwargs):
        device = models.Device.objects.get(id=id)
        name = device.name 
        device.delete()

        return DeleteDevice(
            id,name
        )




class UpdateComponent(graphene.Mutation):
    id = graphene.Int()
    name= graphene.String()
    specification = graphene.Field(SpecificationType) 
    class Arguments:
        id  = graphene.Int()
        name=graphene.String()
        version = graphene.String()
        hw_specification = graphene.String()
        sw_specification = graphene.String()
        support_notes = graphene.String()
        manufacturer_name = graphene.String() 
    def mutate(self,info,id,**kwargs):
        component = models.Component.objects.get(id=id)
        specification = component.specification 
        if kwargs.get('name') is not None :
            component.name = kwargs.get('name')
        if kwargs.get('version') is not None :
        
           specification.version= kwargs.get('version')
        if kwargs.get('hw_specification') is not None :
           specification.hw_specification= kwargs.get('hw_specification')
        if kwargs.get('sw_specification') is not None :
           specification.sw_specification= kwargs.get('sw_specification')
        if kwargs.get('support') is not None :
           specification.support= kwargs.get('support')
        component = component.save()
        specification =specification.save()        

        return UpdateComponent(
            id=component.id,
            name=component.name,
            specification = component.specification,
        )

class DeleteComponent(graphene.Mutation):
    id = graphene.Int()
    name= graphene.String()
    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self,info,id,**kwargs):
        component = models.Component.objects.get(id=id)
        name = component.name 
        component.delete()

        return DeleteComponent(
            id,name
        )


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
        manufacturer_name = graphene.String() 
    def mutate(self,info,name,version,hw_specification,sw_specification,manufacturer_name,support_notes):
        component=models.Component(name=name)
        try:
            manufacturer = models.Manufacturer.objects.get(name=manufacturer_name) 
        except ObjectDoesNotExist:
            manufacturer  = models.Manufacturer.objects.create(name=manufacturer_name)
        specification = models.Specification.objects.create(version=version,hw_specification=hw_specification,
        sw_specification=sw_specification,support_notes=support_notes)
        component.specification = specification
        component.manufacturer = manufacturer
        component.save()
        component.sellers.add(info.context.user)
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
       
        results = models.Device.objects.annotate(search=SearchVector('description'),).filter(search=SearchQuery(query))
        return DeviceSearch(
            devices = results
        )

class ComponentSearch(graphene.Mutation):
    components = graphene.List(ComponentType)

    class Arguments:
        query = graphene.String(required=True)

    def mutate(self,info,query):
       
        results = models.Component.objects.annotate(search=SearchVector('description'),).filter(search=SearchQuery(query))
        return ComponentSearch(
            components= results
        )

class CreateCustomUser(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)

    class Arguments:
        firstname=graphene.String(required=True)
        lastname=graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        #usertype = graphene.String(required=True)
        phone_number = graphene.String() 
    def mutate(self,info,username,password,email,firstname,lastname,**kwargs):
        customuser = models.CustomUser(username=username,email=email,first_name=firstname,last_name=lastname)
        
        if kwargs.get('phone_number') is not None:
            customuser.phone_number = kwargs.get('phone_number')
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
        phone_number = graphene.String()

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
        if kwargs.get('phone_number') is not None:
            customuser.phone_number= kwargs.get('phone_number')

        customuser.name = customuser.first_name + " "+customuser.last_name
        customuser.save()
        return CreateCustomUser(customuser)

class AddressOneUpdate(graphene.Mutation):
    address_one = graphene.Field(AddressOneType)

    class Arguments:
        name = graphene.String()
        phone_number = graphene.String()
        pincode = graphene.String()
        locality = graphene.String()
        address = graphene.String() 
        city_district_town =  graphene.String()
        state = graphene.String()
        landmark = graphene.String()
        address_type = graphene.String()

    def mutate(self,info,**kwargs):
        customuser = info.context.user
        address_one = customuser.address_one
        if kwargs.get('name') is not None:
            address_one.name= kwargs.get('name')
        if kwargs.get('phone_number') is not None:
            address_one.phone_number = kwargs.get('phone_number')
        if kwargs.get('pincode') is not None:
            address_one.pincode= kwargs.get('pincode')
        if kwargs.get('locality') is not None:
            address_one.locality = kwargs.get('locality')
        if kwargs.get('address') is not None:
            address_one.address= kwargs.get('address')
        if kwargs.get('city_district_town') is not None:
            address_one.city_district_town =   kwargs.get('city_district_town') 
        if kwargs.get('state') is not None:
            address_one.state = kwargs.get('state')
        if kwargs.get('landmark') is not None:
            address_one.landmark = kwargs.get('landmark')
        if kwargs.get('address_type') is not None:
            address_one.address_type= kwargs.get('address_type')

        return AddressOneUpdate(address_one)

class AddressTwoUpdate(graphene.Mutation):
    address_two = graphene.Field(AddressTwoType)


    class Arguments:
        name = graphene.String()
        phone_number = graphene.String()
        pincode = graphene.String()
        locality = graphene.String()
        address = graphene.String() 
        city_district_town =  graphene.String()
        state = graphene.String()
        landmark = graphene.String()
        address_type = graphene.String()

    def mutate(self,info,**kwargs):
        customuser = info.context.user
        address_two = customuser.address_two
        if kwargs.get('name') is not None:
            address_two.name= kwargs.get('name')
        if kwargs.get('phone_number') is not None:
            address_two.phone_number = kwargs.get('phone_number')
        if kwargs.get('pincode') is not None:
            address_two.pincode= kwargs.get('pincode')
        if kwargs.get('locality') is not None:
            address_two.locality = kwargs.get('locality')
        if kwargs.get('address') is not None:
            address_two.address= kwargs.get('address')
        if kwargs.get('city_district_town') is not None:
            address_two.city_district_town =   kwargs.get('city_district_town') 
        if kwargs.get('state') is not None:
            address_two.state = kwargs.get('state')
        if kwargs.get('landmark') is not None:
            address_two.landmark = kwargs.get('landmark')
        if kwargs.get('address_type') is not None:
            address_two.address_type= kwargs.get('address_type')

        return AddressTwoUpdate(address_two)




class CreateAddressOne(graphene.Mutation):

    address_one= graphene.Field(AddressOneType)

    class Arguments:
        name = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        pincode = graphene.String(required=True)
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
        return CreateAddressOne(address_one)

class CreateAddressTwo(graphene.Mutation):

    address_two= graphene.Field(AddressTwoType)

    class Arguments:
        name = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        pincode = graphene.String(required=True)
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
class DeviceImage(graphene.Mutation):
    id = graphene.Int()
    path= graphene.String()
    class Arguments:
        id = graphene.Int()
    def mutate(self,info,id,**kwargs):
        device = models.Device.objects.get(id=id)
        file =device.file.document.path
        return DeviceImage(
            id= device.file.id,
            path= file
        )
class CreateDevice(graphene.Mutation):
    id = graphene.Int()
    name=graphene.String()
    reuse_method= graphene.String()
    model_number = graphene.String()
    version = graphene.String()
    hw_specification = graphene.String()
    sw_specification = graphene.String()
    support_notes = graphene.String()
    manufacturer = graphene.Field(ManufacturerType) 
    price  = graphene.String()
    class Arguments:
        document= graphene.Int()
        reuse_method= graphene.String()
        name=graphene.String()
        model_number=graphene.String()
        version = graphene.String(required=True)
        hw_specification = graphene.String(required=True)
        sw_specification = graphene.String(required=True)
        support_notes = graphene.String(required=True)
        manufacturer_name= graphene.String(required=True)
    def mutate(self,info,name,reuse_method,model_number,version,manufacturer_name,hw_specification,sw_specification,support_notes,document):
        print(document) 
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("Not Logged in")
        try:
            manufacturer = models.Manufacturer.objects.get(name=manufacturer_name) 
        except ObjectDoesNotExist:
            manufacturer  = models.Manufacturer.objects.create(name=manufacturer_name)

        device = models.Device(name=name,model_number=model_number,manufacturer=manufacturer,reuse_method=reuse_method)
        device.save()
        specification = models.Specification.objects.create(version=version,hw_specification=hw_specification,sw_specification=sw_specification)
        device.specification = specification
        device.file = models.File.objects.get(id=document)

        device.save() 
        description = "{} {} {} {} {} {}".format(
        device.name,
        device.model_number,
        device.manufacturer,
        device.specification.hw_specification,
        device.specification.sw_specification,
        device.specification.version,
        )
 
        device.specification = specification
        device.description = description
        device.save()
        device.sellers.add(current_user)
        device.save()
        return CreateDevice(
            id=device.id,
            name=device.name,
            version = device.specification.version,
            hw_specification = device.specification.hw_specification,
            sw_specification = device.specification.sw_specification,
            support_notes = device.specification.support_notes,
            reuse_method=device.reuse_method,
            manufacturer =device.manufacturer,
            price = device.price
        )
class CreateManufacturer(graphene.Mutation):
    manufacturer = graphene.Field(ManufacturerType)
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
    def mutate(self,info,name,description):
        manufacturer = models.Manufacturer.objects.create(name=name,description=description)
        return CreateManufacturer(manufacturer)
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
class AddDeviceCart(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    devices = graphene.List(DeviceType)
    class Arguments:
        id = graphene.Int(required=True)
    def mutate(self,info,id):
        buyer= info.context.user
        device = models.Device.objects.get(id=id)
        try :
            cart = models.Cart.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            cart = models.Cart.objects.create(buyer=buyer)
        cart.devices.add(device)
        cart.save()
        devices=cart.devices.all()
        return  AddDeviceCart(
            buyer=buyer,
            devices=devices
        )
class AddDeviceCartQuantity(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    device = graphene.Field(DeviceType)
    quantity = graphene.Int()
    class Arguments:
        id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
    def mutate(self,info,id,quantity):
        buyer= info.context.user
        device = models.Device.objects.get(id=id)
        try :
            cart = models.Cart.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            cart = models.Cart.objects.create(buyer=buyer)
        cart.devices.add(device)
        cart.save()
        try :
            cart_to_device = models.CartToDevice.objects.get(cart=cart,device=device)
        except ObjectDoesNotExist:
            print('iam creating a cart_to_device')
            cart_to_device  = models.CartToDevice.objects.create(cart=cart,device=device,quantity=quantity)
        cart_to_device.quantity =quantity
        cart_to_device.save() 
        return  AddDeviceCartQuantity(
            buyer=cart_to_device.cart.buyer,
            device=cart_to_device.device,
            quantity=cart_to_device.quantity,
        )
'''
class AddComponentCartQuantity(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    component= graphene.Field(ComponentType)
    quantity = graphene.Int()
    class Arguments:
        id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
    def mutate(self,info,id,quantity):
        buyer= info.context.user
        component = models.Component.objects.get(id=id)
        try :
            cart = models.Cart.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            cart = models.Cart.objects.create(buyer=buyer)
        cart.components.add(device)
        cart.save()
        try :
            cart_to_device = models.CartToComponent.objects.get(cart=cart,device=device)
        except ObjectDoesNotExist:
            print('iam creating a cart_to_device')
            cart_to_device  = models.CartToDevice.objects.create(cart=cart,device=device,quantity=quantity)
        cart_to_device.quantity =quantity
        cart_to_device.save() 
        return  AddDeviceCartQuantity(
            buyer=cart_to_device.cart.buyer,
            device=cart_to_device.device,
            quantity=cart_to_device.quantity,
        )


'''

class AddComponentCart(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    components = graphene.List(ComponentType)
    class Arguments:
        id = graphene.Int(required=True)
    def mutate(self,info,id):
        buyer= info.context.user
        component = models.Component.objects.get(id=id)
        try :
            cart = models.Cart.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            cart = models.Cart.objects.create(buyer=buyer)
        cart.components.add(component)
        cart.save()
        components=cart.devices.all()
        return  AddDeviceCart(
            buyer=buyer,
            componenets=components
        )
class AddDeviceWishlist(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    devices = graphene.List(DeviceType)
    class Arguments:
        id = graphene.Int(required=True)
    def mutate(self,info,id):
        buyer = info.context.user
        device = models.Device.objects.get(id=id)
        try :
            wishlist= models.Wishlist.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            wishlist = models.Wishlist.objects.create(buyer=buyer)
        wishlist.devices.add(device)
        wishlist.save()
        devices=wishlist.devices.all()
        return  AddDeviceWishlist(
            buyer=buyer,
            devices=devices
        )
class AddComponentWishlist(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    components = graphene.List(ComponentType)
    class Arguments:
        id = graphene.Int(required=True)
    def mutate(self,info,id):
        buyer = info.context.user
        component = models.Component.objects.get(id=id)
        try :
            wishlist= models.Wishlist.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            wishlist = models.Wishlist.objects.create(buyer=buyer)
        wishlist.components.add(component)
        wishlist.save()
        components=wishlist.components.all()
        return  AddComponentWishlist(
            buyer=buyer,
            components=components
        )


class MoveDeviceWishlist(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    devices = graphene.List(DeviceType)
    class Arguments:
        device= graphene.Int(required=True)
    def mutate(self,info,id):
        buyer= info.context.user
        cart = models.Cart.objects.get(buyer=buyer)
        device = cart.devices.get(id=id) 
        try :
            wishlist= models.Wishlist.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            wishlist = models.Wishlist.objects.create(buyer=buyer)
        wishlist.devices.add(device)
        wishlist.save()
        cart.devices.remove(device)
        cart.save()
        devices=wishlist.devices.all()
        return  MoveDeviceWishlist(
            buyer=buyer,
            devices= devices 
        )

class RemoveDevice(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    device = graphene.Field(DeviceType)
    class Arguments:
        id= graphene.Int(required=True)
    def mutate(self,info,id):
        buyer= info.context.user
        cart = models.Cart.objects.get(buyer=buyer)
        device = cart.devices.get(id=id) 
        cart_device_quantity= models.CartToDevice.objects.get(cart=cart,device=device)
        cart_device_quantity.delete()
        cart.devices.remove(device)
        cart.save()
        return  RemoveDevice(
            buyer=buyer,
            device= device 
        )

class MoveComponentWishlist(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    components= graphene.List(ComponentType)
    class Arguments:
        component= graphene.Int(required=True)
    def mutate(self,info,id):
        buyer= info.context.user
        cart = models.Cart.objects.get(buyer=buyer)
        component= cart.components.get(id=id) 
        try :
            wishlist= models.Wishlist.objects.get(buyer=buyer)
        except ObjectDoesNotExist:
            wishlist = models.Wishlist.objects.create(buyer=buyer)
        wishlist.components.add(component)
        wishlist.save()
        cart.components.remove(component)
        cart.save()
        components=wishlist.componenets.all()
        return  MoveComponentWishlist(
            buyer=buyer,
            components=components 
        )


class CreateOrder(graphene.Mutation):
    buyer = graphene.Field(CustomUserType)
    devices= graphene.List(DeviceType)
    approval = graphene.Boolean()
    class Arguments:
        buyer= CustomUserInput(required=True)
    def mutate(self,info,buyer):
        buyer= models.CustomUser.objects.get(username=buyer.username)
        order = models.Order.objects.create(buyer=buyer)
        cart = models.Cart.objects.get(buyer=buyer)
        devices = cart.devices.all()
        for device in devices:
            order.devices.add(device)
            order.save()
        cart.save()
        devices=cart.devices.all()
        return  CreateOrder(
            buyer=buyer,
            devices=devices,
            approval = order.approval
        )

class DeleteAddressOne(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)
    class Arguments:
        pass
    def mutate(self,info,**kwargs):
        customuser = info.context.user
        address_one  = customuser.address_one
        address_one.delete()
        return DeleteAddressOne(customuser)

class DeleteAddressTwo(graphene.Mutation):
    customuser = graphene.Field(CustomUserType)
    class Arguments:
        pass
    def mutate(self,info,**kwargs):
        customuser = info.context.user
        address_two= customuser.address_two
        address_two.delete()
        return DeleteAddressTwo(customuser)

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
class MoveToCart(graphene.ObjectType):
    device = graphene.Field(DeviceType)

    class Arguments:
        device_id= graphene.Int()

    def mutate(self,info,device_id):
        device = models.Device.objects.get(id=device_id)
        user = info.context.user
        cart = user.cart
        cart.devices.add(device)
        cart.save()
        wishlist = user.wishlist
        wishlist.remove(device)
        wishlist.save()
        return (device)

class Mutation(graphene.ObjectType):
    create_component = CreateComponent.Field()
    create_device = CreateDevice.Field()
    create_customuser=CreateCustomUser.Field() 
    change_password = ChangePassword.Field()   
    add_component = AddComponent.Field()
    add_device_seller = AddDeviceSeller.Field()
    create_banner = CreateBanner.Field()
    add_device_cart= AddDeviceCart.Field()
    move_device_wishlist= MoveDeviceWishlist.Field()
    create_order = CreateOrder.Field()
    approve_order = ApproveOrder.Field()
    add_device_wishlist=AddDeviceWishlist.Field()
    device_search = DeviceSearch.Field()    
    profile_update = ProfileUpdate.Field()
    create_address_one = CreateAddressOne.Field()
    create_address_two = CreateAddressTwo.Field()
    address_one_update = AddressOneUpdate.Field()
    address_two_update = AddressTwoUpdate.Field()
    delete_address_one = DeleteAddressOne.Field()
    delete_address_two = DeleteAddressTwo.Field()
    create_manufacturer = CreateManufacturer.Field()
    update_component   = UpdateComponent.Field()
    delete_component = DeleteComponent.Field()
    component_search = ComponentSearch.Field()
    add_component_cart = AddComponentCart.Field()
    add_component_wishlist = AddComponentWishlist.Field()
    move_component_wishlist = MoveComponentWishlist.Field()
    remove_device = RemoveDevice.Field()
    add_device_cart_quantity=AddDeviceCartQuantity.Field()
    device_image = DeviceImage.Field()