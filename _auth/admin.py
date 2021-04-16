from _auth.models import DefaultUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.


class DefaultUserInline(admin.StackedInline):
    model = DefaultUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (DefaultUserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
