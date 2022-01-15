"""
All Admin configuration related to users

"""
from django.contrib import admin
from django.contrib.auth.admin import Group,GroupAdmin,UserAdmin
from django.utils.text import gettext_lazy as _
from .models import Role,User,AuthTransaction,OTPValidation,SuryamitraProfile
from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()

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

admin.site.site_header = "PVPORT - GIZ"

admin.site.unregister(Group)

admin.site.register(Role, GroupAdmin)
admin.site.register(SuryamitraProfile)
admin.site.register(User, DRFUserAdmin)
admin.site.register(OTPValidation, OTPValidationAdmin)
admin.site.register(AuthTransaction, AuthTransactionAdmin)
