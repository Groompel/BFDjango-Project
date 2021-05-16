from misc.models import Address, BusinessCenter, ResidentialComplex
from rest_framework import serializers as ser


class AddressSerializer(ser.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'district', 'street', 'street_number']


class BusinessCenterSerializer(ser.ModelSerializer):
    class Meta:
        model = BusinessCenter
        fields = '__all__'


class ResidentialComplexSerializer(ser.ModelSerializer):
    class Meta:
        model = ResidentialComplex
        fields = '__all__'
