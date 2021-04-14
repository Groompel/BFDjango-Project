from django.contrib import admin
from .models import CommercialProperty, HouseProperty, FlatProperty

# Register your models here.

admin.site.register(CommercialProperty)
admin.site.register(HouseProperty)
admin.site.register(FlatProperty)
