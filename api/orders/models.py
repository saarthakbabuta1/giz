import imp
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from users.models import User

# Create your models here.

class OrdersModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.JSONField()
    created_date = models.DateTimeField()
    last_updated = models.DateTimeField()
    order_status = models.CharField(max_length=255,default="Ordered")
    amount = models.FloatField(default=0)
    

    class Meta:
        db_table = 'orders'
        verbose_name = _("order")
        verbose_name_plural = _("orders")
    
        def __str__(self):

            return str(self.id) + " | " + str(self.user)

