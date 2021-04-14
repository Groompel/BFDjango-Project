from django.contrib import admin
from .models import BusinessCenter, ResidentialComplex, Address

# Register your models here.

admin.site.register(BusinessCenter)
admin.site.register(ResidentialComplex)
admin.site.register(Address)
