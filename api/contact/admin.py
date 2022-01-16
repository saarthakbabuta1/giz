from operator import imod
from django.contrib import admin
from .models import Contact
from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name","email","mobile")
    search_fields = ["name"]

admin.site.register(Contact,ContactAdmin)
