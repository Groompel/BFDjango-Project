from django.contrib import admin
from .models import Room, BusinessCenter, ResidentialComplex

# Register your models here.

admin.site.register(Room)
admin.site.register(BusinessCenter)
admin.site.register(ResidentialComplex)
