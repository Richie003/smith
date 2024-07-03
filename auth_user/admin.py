from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
from .models import *


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "admin", "username", "tel", "category")
    list_filter = ("admin",)
    fieldsets = (
        (None, {"fields": ("email", "password", "username", "tel", "category")}),
        ("Personal info", {"fields": ()}),
        ("Permissions", {"fields": ("admin",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "tel",
                    "category",
                ),
            },
        ),
    )
    search_fields = ("email", "username", "tel", "category")
    ordering = ("email", "username", "tel", "category")
    filter_horizontal = []


class WeekDayAdmin(admin.ModelAdmin):
    list_display = ("day",)


admin.site.register(User, UserAdmin)
admin.site.register(RestaurantBio)
admin.site.register(CustomerBio)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
admin.site.register(WeekDay, WeekDayAdmin)
