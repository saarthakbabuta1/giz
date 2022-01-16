"""Models for drf-user"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group,PermissionsMixin
from django.db import models
from django.utils.text import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.managers import UserManager
from users.variables import DESTINATION_CHOICES,EMAIL

class Role(Group):
    """
    A proxy model for Group for renaming Group to Role.
    """

    class Meta:
        """Passing model metadata"""

        proxy = True
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents default user model in a Django project.
    Adds following extra attributes:
    mobile: Mobile Number of the user
    name: Name of the user. Replaces last_name & first_name
    update_date: DateTime instance when the user was updated

    """

    username = models.CharField(
        verbose_name=_("Username"), max_length=254, unique=True
    )
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    mobile = models.CharField(
        verbose_name=_("Mobile Number"),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    name = models.CharField(verbose_name=_("Full Name"), max_length=500, blank=False)
    profile_image = models.ImageField(
        verbose_name=_("Profile Photo"), upload_to="user_images", null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name=_("Date Joined"), auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=_("Date Modified"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Activated"), default=False)
    is_staff = models.BooleanField(verbose_name=_("Staff Status"), default=False)

    # Renamed Groups to Roles
    groups = models.ManyToManyField(
        Role,
        verbose_name=_("Roles"),
        blank=True,
        help_text=_(
            "The roles this user belongs to. A user will get all permissions "
            "granted to each of their roles."
        ),
        related_name="user_set",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    class Meta:
        """Passing model metadata"""

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name(self) -> str:
        """Method to return user's full name"""

        return str(self.name)

    def __str__(self):
        """String representation of model"""

        return str(self.username)


class AuthTransaction(models.Model):
    """
    Represents all authentication in the system that took place via
    REST API.

    """

    ip_address = models.GenericIPAddressField(blank=False, null=False)
    token = models.TextField(verbose_name=_("JWT Access Token"))
    session = models.TextField(verbose_name=_("Session Passed"))
    refresh_token = models.TextField(
        blank=True,
        verbose_name=_("JWT Refresh Token"),
    )
    expires_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Expires At")
    )
    create_date = models.DateTimeField(
        verbose_name=_("Create Date/Time"), auto_now_add=True
    )
    update_date = models.DateTimeField(
        verbose_name=_("Date/Time Modified"), auto_now=True
    )
    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT)

    def __str__(self):
        """String representation of model"""

        return str(self.created_by.name) + " | " + str(self.created_by.username)

    class Meta:
        """Passing model metadata"""

        verbose_name = _("Authentication Transaction")
        verbose_name_plural = _("Authentication Transactions")


class OTPValidation(models.Model):
    """
    Represents all OTP Validation in the System.
    """

    otp = models.CharField(verbose_name=_("OTP Code"), max_length=10)
    destination = models.CharField(
        verbose_name=_("Destination Address (Mobile/EMail)"),
        max_length=254,
        unique=True,
    )
    create_date = models.DateTimeField(verbose_name=_("Create Date"), auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=_("Date Modified"), auto_now=True)
    is_validated = models.BooleanField(verbose_name=_("Is Validated"), default=False)
    validate_attempt = models.IntegerField(
        verbose_name=_("Attempted Validation"), default=3
    )
    prop = models.CharField(
        verbose_name=_("Destination Property"),
        default=EMAIL,
        max_length=3,
        choices=DESTINATION_CHOICES,
    )
    send_counter = models.IntegerField(verbose_name=_("OTP Sent Counter"), default=0)
    sms_id = models.CharField(
        verbose_name=_("SMS ID"), max_length=254, null=True, blank=True
    )
    reactive_at = models.DateTimeField(verbose_name=_("ReActivate Sending OTP"))

    def __str__(self):
        """String representation of model"""

        return self.destination

    class Meta:
        """Passing model metadata"""

        verbose_name = _("OTP Validation")
        verbose_name_plural = _("OTP Validations")

class SuryamitraProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,editable=False)
    registeration_id = models.CharField(max_length=150,unique=True)
    certificate_copy = models.ImageField()

    class Meta:
        db_table = 'suryamitra'
        verbose_name = _("Suryamitra")
        verbose_name_plural = _("Suryamitra")

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("Instance: ",instance)
        print(sender.objects.filter(username = instance).values('groups')[0])
        group = sender.objects.filter(username = instance).values('groups')[0]['groups']
        print(group)
        if group == "1":
            SuryamitraProfile.objects.create(user=instance,registeration_id="123456")
        elif group == "2":
            print("vendor")
        elif group == None:
            print("No group")