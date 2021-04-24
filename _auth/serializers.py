from rest_framework import serializers
from .models import DefaultUser


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)


class DefaultUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DefaultUser
        fields = '__all__'
