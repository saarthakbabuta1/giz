from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Models(models.Model):
    sku = models.CharField(primary_key= True,max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'pv_models'
        verbose_name = _("Model")
        verbose_name_plural = _("Models")

    def __str__(self):
        return self.name

class Products(models.Model):
    sku = models.CharField(primary_key=True,max_length=10)
    oem = models.CharField(max_length=255)
    quantity = models.IntegerField()
    assembly = models.TextField()
    comments = models.TextField(blank=True)
    sku_model = models.ForeignKey(Models,on_delete=models.CASCADE)

    class Meta:
        db_table = 'pv_products'
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


    def __str__(self):
        return self.assembly

    




