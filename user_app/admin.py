from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile
# Register your models here.
# admin.site.register(Profile)


class UserAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False  # Deny edit permission for all users
    
admin.site.register(Profile, UserAdmin)


class CustomUserAdmin(UserAdmin):
    def has_change_permission(self, request, obj=None):
        return False  # Deny edit permission for all users


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
