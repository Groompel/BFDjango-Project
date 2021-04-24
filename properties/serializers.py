from properties.models import CommercialProperty, FlatProperty, HouseProperty
from misc.serializers import AddressSerializer, BusinessCenterSerializer, ResidentialComplexSerializer
from rest_framework import serializers as ser

PROPERTY_BASE_FIELDS = ['price', 'area', 'built_year',
                        'exploitation_year', 'address', 'number_of_rooms', 'description']

LIVING_PROPERTY_BASE_FIELDS = PROPERTY_BASE_FIELDS + \
    ['kitchen_area', 'construction_type', 'number_of_bedrooms']


class CommercialPropertySerializer(ser.ModelSerializer):
    business_center = BusinessCenterSerializer()

    class Meta:
        model = CommercialProperty
        fields = PROPERTY_BASE_FIELDS + ['business_center']


class HousePropertySerializer(ser.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = HouseProperty
        fields = LIVING_PROPERTY_BASE_FIELDS + \
            ['land_area', 'number_of_floors']


class FlatPropertySerializer(ser.ModelSerializer):
    address = AddressSerializer()
    residential_complex = ResidentialComplexSerializer()

    class Meta:
        model = FlatProperty
        fields = LIVING_PROPERTY_BASE_FIELDS + \
            ['floor', 'number_of_floors_in_house', 'residential_complex']
