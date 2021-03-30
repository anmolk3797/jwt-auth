from django.contrib import admin
from apps.authentication.models import User, UserPermissions
from django.contrib.auth.models import Group

admin.site.site_header = "pet_hotel"
# admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    search_fields = ["email", "first_name"]
    ordering = ["created_at"]
    list_display = ["id", "first_name", "email", "created_at"]


admin.site.register(User, UserAdmin)
admin.site.register(UserPermissions)
