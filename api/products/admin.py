from django.contrib import admin
from .models import Models,Products
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):


    list_display = ("sku", "oem","sku_model", "quantity")
    search_fields = ["oem"]

class ModelsAdmin(admin.ModelAdmin):


    list_display = ("sku", "name", "brand")
    search_fields = ["name"]


admin.site.register(Models,ModelsAdmin)
admin.site.register(Products,ProductsAdmin)
