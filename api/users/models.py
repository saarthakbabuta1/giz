"""Models for drf-user"""
from re import T
from tabnanny import verbose
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group,PermissionsMixin
from django.db import models
from django.utils.text import gettext_lazy as _
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from users.managers import UserManager
from users.variables import DESTINATION_CHOICES,EMAIL
from django.forms.models import model_to_dict

class Role(Group):
    """
    A proxy model for Group for renaming Group to Role.
    """

    class Meta:

        proxy = True
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

        def __str__(self):
            return self.name


class User(AbstractBaseUser, PermissionsMixin):

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
        verbose_name=_("Profile Photo"), upload_to="./users/images/users/", null=True, blank=True)
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
        related_query_name="user"
    )

    objects = UserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    class Meta:
        """Passing model metadata"""

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name(self) -> str:
        return str(self.name)

    def get_group(self) -> str:
        group_name = str(self.groups.values('name').first())[10:]
        group_name = group_name[:-2]
        print(group_name)
        return str(group_name)

    def __str__(self):
        return str(self.username) 


class AuthTransaction(models.Model):

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

class SuryamitraProfile(User):
    registeration_id = models.CharField(max_length=255,blank=True,null=True)
    certificate = models.ImageField(upload_to='./users/images/suryamitra/',blank=True,null=True)
    def save(self):
        self.is_active = True
        self.is_staff = True
        self.set_password(self.password)
        super(SuryamitraProfile, self).save()
        self.groups.set(['1'])
    class Meta:
        db_table = 'suryamitra'
        verbose_name = _("Suryamitra")
        verbose_name_plural = _("Suryamitra")

    def __str__(self):
        return str(self.username)

class VendorProfile(User):
    registeration_id = models.CharField(max_length=255,verbose_name=_("Registeration ID"),blank=True,null=True)
    contact_person = models.CharField(max_length=255,blank=True,null=True)
    contact_number = models.CharField(
        verbose_name=_("Contact Number"),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )

    def save(self):
        self.is_active = True
        self.is_staff = True
        self.set_password(self.password)
        super(VendorProfile, self).save()
        self.groups.set(['2'])
    class Meta:
        db_table = 'vendor'
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendor")

    def __str__(self):
        return str(self.username)


class TechSupportProfile(User):
    tech_support_log = models.CharField(max_length=255,blank=True,null=True)

    def save(self):
        self.is_active = True
        self.is_staff=True
        self.set_password(self.password)
        super(TechSupportProfile,self).save()
        self.groups.set(['5'])

        class Meta:
            db_table = 'tech_support'
            verbose_name = _("Tech Support")
            verbose_name_plural = _("Tech Support")
        
        def __str__(self):
            return str(self.name)

class DiscomProfile(User):
    code = models.CharField(max_length=255,unique=True,verbose_name=_("Discom Code"))
    
    def save(self):
        self.is_active = True
        self.is_staff=True
        self.set_password(self.password)
        super(DiscomProfile,self).save()
        self.groups.set(['6'])

        class Meta:
            db_table = 'discom'
            verbose_name = _("Discom")
            verbose_name_plural = _("Discom")
        
        def __str__(self):
            return str(self.code)


class CustomerProfile(User):
    address_line_1 = models.CharField(max_length=255,blank=True,null=True,verbose_name=_("Address Line 1"))
    address_line_2 = models.CharField(max_length=255,blank=True,null=True,verbose_name=_("Address Line 2"))
    city = models.CharField(max_length=255,blank=True,null=True,verbose_name=_("City"))
    state = models.CharField(max_length=255,blank=True,null=True,verbose_name=_("State"))
    address_country = models.CharField(max_length=255,blank=True,null=True,verbose_name=_("Country"),default="India")
    pin_code = models.CharField(max_length=9,blank=True,null=True,verbose_name=_("PinCode"))
    discom_code = models.ForeignKey(DiscomProfile,on_delete=models.CASCADE,verbose_name=_("Discom"),null=True)
    ca_number = models.CharField(max_length=255,blank=True,null=True,verbose_name=_("CA Number"))

    def save(self):
        self.is_active=True
        self.is_staff=True
        self.set_password(self.password)
        super(CustomerProfile,self).save()
        self.groups.set(['4'])
    
    class Meta:
        db_table = 'customer'
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self):
        return str(self.name)


# class Address(models.Model):
#     TYPES_CHOICES = (
#         ('HOME','Home'),
#         ('WORK','Work'),
#         ('OTHER','Other')
#     )
#     street_line1 = models.CharField(_('Address 1'), max_length = 100, blank = True)
#     street_line2 = models.CharField(_('Address 2'), max_length = 100, blank = True)
#     zipcode = models.CharField(_('ZIP code'), max_length = 9, blank = True)
#     city = models.CharField(_('City'), max_length = 100, blank = True)
#     state = models.CharField(_('State'), max_length = 100, blank = True)

#     class Meta:
#         db_table = 'address'
#         verbose_name = _("Addressess")
#         verbose_name_plural = _("Address")
    
#     def __str__(self) -> str:
#         return str(self.user)