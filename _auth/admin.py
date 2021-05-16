from _auth.models import Agency, Agent, DefaultUser
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


class AgentInline(admin.StackedInline):
    model = Agent
    extra = 1


class AgencyAdmin(admin.ModelAdmin):
    inlines = (AgentInline, )


admin.site.register(Agency, AgencyAdmin)
admin.site.register(Agent)
