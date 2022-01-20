from django.contrib import admin
from .models import Models,Products
from django.contrib.admin.models import LogEntry
from django.utils.text import gettext_lazy as _

class ProductsAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(""), {"fields": ("sku", "oem","assembly","quantity","available_quantity","comments")}),
      
    )

    list_display = ("sku", "oem","quantity","available_quantity")
    search_fields = ["sku","oem"]
    #readonly_fields = ["quantity"]

class ModelsAdmin(admin.ModelAdmin):

    list_display = ("sku", "name", "brand")
    search_fields = ["sku","name"]
    filter_horizontal = ('components',)


admin.site.register(Models,ModelsAdmin)
admin.site.register(Products,ProductsAdmin)

LogEntry.objects.all().delete()