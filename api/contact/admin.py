from operator import imod
from django.contrib import admin
from .models import Contact

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name","email","mobile")
    search_fields = ["name"]

admin.site.register(Contact,ContactAdmin)
