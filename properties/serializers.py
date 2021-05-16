from misc.models import Address, ResidentialComplex
from _auth.models import DefaultUser
from _auth.serializers import DefaultUserSerializer, UserSerializer
from rest_framework.fields import IntegerField
from properties.models import CommercialProperty, FlatProperty, HouseProperty
from misc.serializers import AddressSerializer, BusinessCenterSerializer, ResidentialComplexSerializer
from rest_framework import serializers as ser
from django.contrib.auth.models import User
from .models import BusinessCenter

PROPERTY_BASE_FIELDS = ['id', 'user', 'user_detail', 'image', 'deal_type', 'price', 'area', 'built_year',
                        'exploitation_year', 'address', 'number_of_rooms', 'description']

LIVING_PROPERTY_BASE_FIELDS = PROPERTY_BASE_FIELDS + \
    ['kitchen_area', 'construction_type', 'number_of_bedrooms']


class BasePropertySerializer(ser.ModelSerializer):
    user_detail = DefaultUserSerializer(source='user', read_only=True)
    user = IntegerField(write_only=True)
    address = AddressSerializer(read_only=True)


class BasePropertyCreateSerializer(ser.Serializer):
    user_detail = DefaultUserSerializer(source='user', read_only=True)
    user = IntegerField(write_only=True)
    address = AddressSerializer(write_only=True)


class CommercialPropertyCreateSerializer(BasePropertyCreateSerializer):
    business_center = IntegerField(write_only=True)

    class Meta:
        model = CommercialProperty
        fields = PROPERTY_BASE_FIELDS + \
            ['business_center', 'business_center_detail']

    def create(self, validated_data):
        business_center = BusinessCenter.objects.get(
            id=validated_data.pop('business_center'))
        user = DefaultUser.objects.get(id=validated_data.pop('user'))
        address = Address.objects.get_or_create(
            **validated_data.pop('address'))[0]
        return CommercialProperty.objects.create(business_center=business_center, user=user, address=address,  **validated_data)


class CommercialPropertySerializer(BasePropertySerializer):
    business_center_detail = BusinessCenterSerializer(
        read_only=True, source='business_center')
    business_center = IntegerField(write_only=True)

    class Meta:
        model = CommercialProperty
        fields = PROPERTY_BASE_FIELDS + \
            ['business_center', 'business_center_detail']

    def update(self, instance, validated_data):
        business_center = BusinessCenter.objects.get(
            id=validated_data.pop('business_center', instance.business_center))
        validated_data.pop('user')

        setattr(instance, 'business_center', business_center)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class HousePropertyCreateSerializer(BasePropertyCreateSerializer):
    class Meta:
        model = HouseProperty
        fields = LIVING_PROPERTY_BASE_FIELDS + \
            ['land_area', 'number_of_floors']

    def create(self, validated_data):
        user = DefaultUser.objects.get(id=validated_data.pop('user'))
        address = Address.objects.get_or_create(
            **validated_data.pop('address'))[0]
        return HouseProperty.objects.create(user=user, address=address, **validated_data)


class HousePropertySerializer(BasePropertySerializer):

    class Meta:
        model = HouseProperty
        fields = LIVING_PROPERTY_BASE_FIELDS + \
            ['land_area', 'number_of_floors']

    def update(self, instance, validated_data):
        validated_data.pop('user')

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class FlatPropertyCreateSerializer(BasePropertyCreateSerializer):
    residential_complex = IntegerField(write_only=True)

    class Meta:
        model = FlatProperty
        fields = LIVING_PROPERTY_BASE_FIELDS + \
            ['floor', 'number_of_floors_in_house', 'residential_complex']

    def create(self, validated_data):
        residential_complex = ResidentialComplex.objects.get(
            id=validated_data.pop('residential_complex'))
        user = DefaultUser.objects.get(id=validated_data.pop('user'))
        address = Address.objects.get_or_create(
            **validated_data.pop('address'))[0]
        return FlatProperty.objects.create(user=user, residential_complex=residential_complex, address=address, **validated_data)


class FlatPropertySerializer(BasePropertySerializer):
    residential_complex_detail = ResidentialComplexSerializer(
        source='residential_complex', read_only=True)

    class Meta:
        model = FlatProperty
        fields = LIVING_PROPERTY_BASE_FIELDS + \
            ['floor', 'number_of_floors_in_house', 'residential_complex_detail']

    def update(self, instance, validated_data):
        validated_data.pop('user')
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
