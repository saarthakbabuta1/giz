from operator import imod
from django.contrib import admin
from .models import Contact
from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name","email","mobile")
    search_fields = ["name"]
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Contact,ContactAdmin)
