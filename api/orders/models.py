import imp
from operator import imod
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from users.models import SuryamitraProfile
from users.models import User

# Create your models here.

class OrdersModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=255,default="Ordered")
    amount = models.FloatField(default=0)
    delivery_location = models.CharField(max_length=255,blank=True,null=True)
    discom = models.CharField(max_length=255,blank=True,null=True)
    ca_number = models.CharField(max_length=255,blank=True,null=True)
    order_confirmation = models.CharField(max_length=255,blank=True,null=True)
    delivery_timeline = models.DateTimeField(blank=True,null=True)
    tech_contact_information = models.CharField(max_length=255,blank=True,null=True)
    suryamitra = models.ForeignKey(to=SuryamitraProfile,on_delete = models.CASCADE,
    blank=True,null=True)

    class Meta:
        db_table = 'orders'
        verbose_name = _("order")
        verbose_name_plural = _("orders")
    
        def __str__(self):

            return str(self.id) + " | " + str(self.user)

