from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import DrChronoAuth

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class DrChronoAuthInline(admin.StackedInline):
    model = DrChronoAuth
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (DrChronoAuthInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
