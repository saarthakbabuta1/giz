"""
All Admin configuration related to users

"""
from django.contrib import admin
from django.contrib.auth.admin import Group,GroupAdmin,UserAdmin
from django.utils.text import gettext_lazy as _
from .models import Role,User,AuthTransaction,OTPValidation,SuryamitraProfile,VendorProfile
from .models import CustomerProfile,TechSupportProfile,DiscomProfile
from django.contrib.admin.models import LogEntry
from django.contrib import messages
from django.contrib.sites.models import Site

class DRFUserAdmin(UserAdmin):
    """
    Overrides UserAdmin to show fields name & mobile and remove fields:
    first_name, last_name
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "profile_image", "email", "mobile")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "update_date")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name","email", "mobile","is_active","is_staff","password1", "password2",
                "groups"),
            },
        ),
    )
    list_display = ("username", "email", "name", "mobile", "is_staff")
    search_fields = ("username", "name", "email", "mobile")
    readonly_fields = ("date_joined", "last_login", "update_date")
    
    def make_active(modeladmin, request, queryset):
        queryset.update(is_active = 1)
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!")
  
    def make_inactive(modeladmin, request, queryset):
        queryset.update(is_active = 0)
        messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")
    actions = [make_active,make_inactive]


class OTPValidationAdmin(admin.ModelAdmin):
    """OTP Validation Admin"""

    list_display = ("destination", "otp", "prop")


class AuthTransactionAdmin(admin.ModelAdmin):
    """AuthTransaction Admin"""

    list_display = ("created_by", "ip_address", "create_date")

    def has_add_permission(self, request):
        """Limits admin to add an object."""

        return False

    def has_change_permission(self, request, obj=None):
        """Limits admin to change an object."""

        return False

    def has_delete_permission(self, request, obj=None):
        """Limits admin to delete an object."""

        return False

class SuryamitrAdmin(admin.ModelAdmin):
    list_display=('name',"email")
    fieldsets = (
        (_("Authentication info"), {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "profile_image", "email", "mobile","registeration_id","certificate")}),
      
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name","email", "mobile","password1", "password2"),
            },
        ),
    )

class VendorAdmin(admin.ModelAdmin):
    list_display=('name',"email")
    fieldsets = (
        (_("Authentication info"), {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "profile_image", "email", "mobile")}),
        (_("Vendor info"),{"fields":("contact_person","contact_number")})
      
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name","email", "mobile","password1", "password2"),
            },
        ),
    )

class CustomerAdmin(admin.ModelAdmin):
    list_display=('name',"email")
    fieldsets = (
        (_("Authentication info"), {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "mobile","profile_image")}),
        (_("Adress info"),{"fields":(("address_line_1","address_line_2","city","state","address_country","pin_code"))}),
        (_("Other info"),{"fields": ("discom_code","ca_number")}),
      
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name","email", "mobile","password1", "password2"),
            },
        ),
    )

class TechSupportAdmin(admin.ModelAdmin):
    list_display=('name',"email")
    fieldsets = (
        (_("Authentication info"), {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "mobile","profile_image","tech_support_log")}),
      
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name","email", "mobile","password1", "password2"),
            },
        ),
    )

class DiscomAdmin(admin.ModelAdmin):
    list_display=('name',"email")
    fieldsets = (
        (_("Authentication info"), {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "mobile","code")}),
      
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name","email", "mobile","password1", "password2"),
            },
        ),
    )

admin.site.site_header = "PVPORT - GIZ"
admin.site.site_title = "PVPORT"
admin.site.index_title = "Admin Panel"
admin.site.site_url = None


admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(SuryamitraProfile,SuryamitrAdmin)
admin.site.register(VendorProfile,VendorAdmin)
admin.site.register(CustomerProfile,CustomerAdmin)
admin.site.register(TechSupportProfile,TechSupportAdmin)
admin.site.register(DiscomProfile,DiscomAdmin)
# admin.site.register(Role,GroupAdmin)
LogEntry.objects.all().delete()