import os
import uuid
from django.db import models
from django.conf import settings
from core.utils.models import DateTimeRange, NameFieldInjector, TimeStamp, UUIDInjector
from django.utils.translation import gettext as _

from core.utils.exceptions import ExtensionNotAcceptableError

User = settings.AUTH_USER_MODEL

# Create your models here.

def room_featured_image_path(_, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    allowed_ext = [
        'png', 'jpg',
        'jpeg']

    if not ext.lower() in allowed_ext:
        raise ExtensionNotAcceptableError(ext)

    return os.path.join('uploads/rooms/', filename)


class Customer(UUIDInjector, TimeStamp, NameFieldInjector):
    email = models.CharField(max_length=2500, null=True, blank=True, unique=True)
    code = models.CharField(max_length=20)
    pass_code = models.CharField(max_length=100)
    updated_by = models.ForeignKey(User,
                                   related_name="client_modifier",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_client", _("Can approve client")),
                    )


class RoomService(UUIDInjector, TimeStamp, NameFieldInjector):
    caption = models.CharField(max_length=100)
    material_icon_code = models.CharField(max_length=50)
    updated_by = models.ForeignKey(User,
                                   related_name="room_service_modifier",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_roomservice", _("Can approve room service")),
                    )


class Room(UUIDInjector, TimeStamp, NameFieldInjector):
    price = models.FloatField(default=0.00)
    description = models.TextField()
    featured_image = models.ImageField(null=True, blank=True,
                                upload_to=room_featured_image_path)
    services = models.ManyToManyField(RoomService, blank=True)
    updated_by = models.ForeignKey(User,
                                   related_name="room_modifier",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_room", _("Can approve room")),
                    )


class Booking(UUIDInjector, TimeStamp, NameFieldInjector, DateTimeRange):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    number_of_people = models.IntegerField(default=1, null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   related_name="booking_modifier",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_booking", _("Can approve booking")),
                    )

class Coupon(UUIDInjector, TimeStamp, NameFieldInjector, DateTimeRange):
    code = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   related_name="coupon_modifier",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_coupon", _("Can approve coupon")),
                    )


class SpecialOffer(UUIDInjector, TimeStamp, NameFieldInjector, DateTimeRange):
    description = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   related_name="spacial_offer_modifier",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_specialoffer", _("Can approve special offer")),
                    )
        
class Banner(UUIDInjector, TimeStamp, NameFieldInjector):
    title = models.CharField(max_length=100)
    slogan = models.CharField(max_length=100)
    default = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   related_name="banner_modifier",
                                   on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_banner", _("Can approve banner")),
                    )


class Activity(UUIDInjector, TimeStamp, NameFieldInjector):
    in_slider = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    image_alt = models.CharField(max_length=150, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True,
                                upload_to=room_featured_image_path)
    updated_by = models.ForeignKey(User,
                                   related_name="activity_modifier",
                                   on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_activity", _("Can approve activity")),
                    )
        

class Strength(UUIDInjector, TimeStamp, NameFieldInjector):
    in_slider = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    image_alt = models.CharField(max_length=150, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True,
                                upload_to=room_featured_image_path)
    updated_by = models.ForeignKey(User,
                                   related_name="strength_modifier",
                                   on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_strength", _("Can approve strength")),
                    )
        

class Kitchen(UUIDInjector, TimeStamp, NameFieldInjector):
    title = models.CharField(max_length=100)
    excerpt = models.TextField(max_length=500, null=True, blank=True)
    default = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   related_name="kitchen_modifier",
                                   on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_kitchen", _("Can approve kitchen")),
                    )
        

class Gallery(UUIDInjector, TimeStamp, NameFieldInjector):
    title = models.CharField(max_length=100)
    default = models.BooleanField(default=False, null=True, blank=True)
    excerpt1_title = models.CharField(max_length=100)
    excerpt1 = models.TextField(null=True, blank=True)
    excerpt2_title = models.CharField(max_length=100)
    excerpt2 = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   related_name="gallery_modifier",
                                   on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_gallery", _("Can approve gallery")),
                    )


class Service(UUIDInjector, TimeStamp, NameFieldInjector):
    in_slider = models.BooleanField(default=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    material_icon_code = models.CharField(max_length=50, null=True, blank=True)
    image_alt = models.CharField(max_length=150, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True,
                                upload_to=room_featured_image_path)
    updated_by = models.ForeignKey(User,
                                   related_name="kitchen_service",
                                   on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        permissions = (
                    ("approve_service", _("Can approve service")),
                    )