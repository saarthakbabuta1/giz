from zoneinfo import available_timezones
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Products(models.Model):
    sku = models.CharField(primary_key=True,max_length=10,verbose_name=_("SKU"))
    oem = models.CharField(max_length=100,verbose_name=_("OEM"))
    quantity = models.IntegerField(verbose_name=_("Required Qty"))
    available_quantity = models.IntegerField(verbose_name=_("Available Qty"),default=0)
    assembly = models.TextField()
    comments = models.TextField(blank=True)

    class Meta:
        db_table = 'pv_products'
        verbose_name = _("Component")
        verbose_name_plural = _("Components")
        ordering = ['sku']


    def __str__(self):
        return str(self.sku) + " | " + str(self.assembly)


class Models(models.Model):
    sku = models.CharField(primary_key= True,max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.CharField(max_length=255)
    grid = models.CharField(max_length=255,choices=[('Off Grid', 'Off Grid'), ('On Grid', 'On Grid')],
    blank=True,null=True)
    components = models.ManyToManyField(Products,verbose_name=_("Compnents"), related_name="component_set",
        related_query_name="component")

    class Meta:
        db_table = 'pv_models'
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['sku']

    def __str__(self):
        return self.name
    




