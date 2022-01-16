import imp
from django.contrib import admin
from .models import OrdersModel

from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()
# Register your models here.


class OrdersAdmin(admin.ModelAdmin):
    list_display = ("user","order_status","created_date")
    search_fields = ["order_status"]

admin.site.register(OrdersModel,OrdersAdmin)