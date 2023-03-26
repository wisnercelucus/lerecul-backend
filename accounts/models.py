import os
import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext as _
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import Permission

from core.utils.models import UUIDInjector, TimeStamp
from django.conf import settings

from core.utils.exceptions import ExtensionNotAcceptableError
from frontend_views.models import FrontEndMenuLink


def user_group_image_path(instance, filename):
    ext = filename.split('.')[-1]
    allowed_ext = ['jpg', 'jpeg', 'gif', 'png']
    if not ext.lower() in allowed_ext:
        raise ExtensionNotAcceptableError(ext)
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/profile/', filename)

LANGUAGES = (
    ('en', _('English')),
    ('fr', _("French")),
    ('es', _("Spanish")),
)

SEX_CHOICES = (
    ("male", _('Male')),
    ("female", _('Male')),
    ("other", _('Other')),
    ("no mention", _('No mention')),
)

GROUP_CONFIDENTIALITY_CHOICES = (
    ("private", _('Private')),
    ("public", _('Public')),
)


def account_avatar_path(_, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    allowed_ext = [
        'png', 'jpg',
        'jpeg']

    if not ext.lower() in allowed_ext:
        raise ExtensionNotAcceptableError(ext)

    return os.path.join('uploads/acounts/avatars/', filename)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin_user(self, username, email, password):
        """Creates and saves a new super user"""
        username = username.lower()
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_admin = True
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))

        return self.create_user(email, password, **extra_fields)
        

class UserRole(UUIDInjector):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    frontend_views = models.ManyToManyField(FrontEndMenuLink, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='user_role_creator',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='user_role_modifier',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
                    ("approve_userrole", _("Can approve user role")),
                    )

        #verbose_name_plural = "geographies"

class UserPosition(UUIDInjector):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='user_position_creator',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='user_position_modifier',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
                    ("approve_userposition", _("Can approve user position")),
                    )

        #verbose_name_plural = "geographies"

class User(AbstractBaseUser, PermissionsMixin, UUIDInjector):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    notified_on_new_booking = models.BooleanField(default=False, null=True, blank=True)
    primary_contact_for_customer_care = models.BooleanField(default=False, null=True, blank=True)
    #notified_on_learning_notes = models.BooleanField(default=False, null=True, blank=True)
    #notified_on_stories = models.BooleanField(default=False, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255, blank=True, null=True)
    roles = models.ManyToManyField(UserRole, blank=True)
    frontend_views = models.ManyToManyField(FrontEndMenuLink, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    new_account_notified = models.BooleanField(default=False)
    preferred_language = models.CharField(choices=LANGUAGES, default='en', max_length=30, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_user_all_permissions(self):
        permissions = []
        for role in self.roles.all():
            for perm in role.permissions.all():
                permissions.append(perm)

        for perm in self.user_permissions.all():
            if not perm in permissions:
              permissions.append(perm)
        return set(permissions)

    def get_user_all_frontend_views(self):
        views = []
        for role in self.roles.all():
            for v in role.frontend_views.all():
                views.append(v)

        for v in self.frontend_views.all():
            if not v in views:
              views.append(v)
        return set(views)


    def get_user_permission_codes(self):
        user_permissions = self.get_user_all_permissions()
        perm_codes = [p.content_type.app_label +'.'+ p.codename for p in user_permissions]
        return perm_codes

    def has_permissions(self, perms):
        user_permission_code = self.get_user_permission_codes()
        perm_in = [perm in user_permission_code for perm in perms]
        return False not in perm_in
            
    def has_permission(self, perm):
        user_permission_code = self.get_user_permission_codes()
        return perm in user_permission_code


    class Meta:
        permissions = (
                    ("approve_user", _("Can approve user")),
                    ("activate_user", _("Can activate user")),
                    ("deactivate_user", _("Can deactivate user")),
                    )

        #verbose_name_plural = "geographies"

class UserProfile(TimeStamp, UUIDInjector):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    #approver = models.ForeignKey(User, related_name='user_record_approver', blank=True, null=True, on_delete=models.SET_NULL)
    email = models.CharField(_('email address'), max_length=250, unique=True, null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    sex = models.CharField(max_length=150, choices=SEX_CHOICES, null=True, blank=True)
    phone_home = models.CharField(max_length=150, null=True, blank=True)
    phone_work = models.CharField(max_length=150, null=True, blank=True)
    phone_mobile = models.CharField(max_length=150, null=True, blank=True)

    apt_number = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    notified_on_new_booking = models.BooleanField(default=False, null=True, blank=True)
    primary_contact_for_customer_care = models.BooleanField(default=False, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)
    joined_on = models.DateField(null=True, blank=True)
    roles = models.ManyToManyField(UserRole, blank=True)
    position = models.ForeignKey(UserPosition, on_delete=models.SET_NULL, blank=True, null=True)

    quote = models.TextField(null=True, blank=True)
    quote_author = models.CharField(max_length=250, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    moto = models.CharField(max_length=250, null=True, blank=True)
    linkedin_profile_link = models.CharField(max_length=250, null=True, blank=True)
    facebook_profile_link = models.CharField(max_length=250, null=True, blank=True)
    twitter_profile_link = models.CharField(max_length=250, null=True, blank=True)
    instagram_profile_link = models.CharField(max_length=250, null=True, blank=True)
    quora_profile_link = models.CharField(max_length=250, null=True, blank=True)
    github_profile_link = models.CharField(max_length=250, null=True, blank=True)
    reddit_profile_link = models.CharField(max_length=250, null=True, blank=True)

    updated_by = models.ForeignKey(User,
                                   related_name="profile_modifier",
                                   on_delete=models.CASCADE, null=True)

    avatar=models.FileField(max_length=500,
                                null=True, blank=True,
                                upload_to=account_avatar_path)

    def __str__(self):
        return self.user.email

    class Meta:
        permissions = (
                    ("approve_userprofile", _("Can approve user profile")),
                    )

        #verbose_name_plural = "geographies"


def user_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user = instance
        email = user.email
        username = email.split('@')[0]
        user.username = username 
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()
        user.save()
        

def profile_save_receiver(sender, instance, created, *args, **kwargs):
    user = instance.user
    if instance.last_name and instance.first_name:
        user.name = instance.last_name.upper() + ' ' + instance.first_name
        user.save()

post_save.connect(user_save_receiver, sender=User)
post_save.connect(profile_save_receiver, sender=UserProfile)