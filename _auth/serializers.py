from re import I
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField
from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Agency, Agent, DefaultUser


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)


class DefaultUserCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    password = CharField(max_length=255, write_only=True)
    email = CharField(max_length=255, write_only=True)
    username = CharField(max_length=255, write_only=True)

    class Meta:
        model = DefaultUser
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.pop('username'),
                                        password=validated_data.pop(
                                            'password'),
                                        email=validated_data.pop('email'))

        return DefaultUser.objects.create(user=user, **validated_data)


class DefaultUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    password = CharField(max_length=255, write_only=True, required=False)
    email = CharField(max_length=255, write_only=True, required=False)

    class Meta:
        model = DefaultUser
        fields = '__all__'

    def get_validation_exclusions(self):
        exclusions = super(DefaultUserSerializer,
                           self).get_validation_exclusions()
        return exclusions + ['password', 'email']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)

        if (password != None):
            instance.user.set_password(password)
            instance.user.save()

        if (email != None):
            setattr(instance.user, 'email', email)
            instance.user.save()

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class AgentSerializer(serializers.ModelSerializer):
    user = DefaultUserSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = '__all__'


class AgencySerializer(serializers.ModelSerializer):
    agents = AgentSerializer(many=True, read_only=True)
    owner_detail = DefaultUserSerializer(read_only=True, source='owner')
    owner = IntegerField(write_only=True)

    class Meta:
        model = Agency
        fields = ['id', 'name', 'owner', 'owner_detail', 'agents', ]

    def create(self, validated_data):
        data = validated_data.copy()
        data['owner'] = DefaultUser.objects.get(
            id=validated_data.pop('owner'))

        return super().create(data)
