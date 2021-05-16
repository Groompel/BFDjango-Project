from rest_framework.response import Response
from _auth.models import DefaultUser
from misc.models import Address
from django.shortcuts import render
from rest_framework import status, viewsets, permissions
from properties.models import CommercialProperty, FlatProperty, HouseProperty
from properties.serializers import CommercialPropertyCreateSerializer, CommercialPropertySerializer, FlatPropertyCreateSerializer, FlatPropertySerializer, HousePropertyCreateSerializer, HousePropertySerializer
from django.forms.models import model_to_dict
import logging

logger = logging.getLogger(__name__)

# Create your views here.


class CommercialProperyViewSet(viewsets.ModelViewSet):
    queryset = CommercialProperty.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CommercialPropertyCreateSerializer
        return CommercialPropertySerializer

    def get_permissions(self):
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request_user = DefaultUser.objects.get(user=request.user)
        address_data = request.data['address']
        address = Address.objects.get_or_create(
            city=address_data['city'],
            district=address_data['district'],
            street=address_data['street'],
            street_number=address_data['street_number'])[0]

        request.data['user'] = request_user.id
        request.data['address'] = model_to_dict(address)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            request_user = DefaultUser.objects.get(user=request.user)
            prop = CommercialProperty.objects.get(id=pk)
            request.data['user'] = request_user.id

            if (prop.user.id != request_user.id):
                return Response({'error': 'You are not allowed to update this post.'}, status=status.HTTP_401_UNAUTHORIZED)

        except (DefaultUser.DoesNotExist, CommercialProperty.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            request_user = DefaultUser.objects.get(user=request.user)
            prop = CommercialProperty.objects.get(id=pk)

            if (prop.user.id != request_user.id):
                return Response({'error': 'You are not allowed to delete this post.'}, status=status.HTTP_401_UNAUTHORIZED)

        except (DefaultUser.DoesNotExist, CommercialProperty.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().delete(request, *args, **kwargs)


class HousePropertyViewSet(viewsets.ModelViewSet):
    queryset = HouseProperty.objects.all()
    serializer_class = HousePropertySerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return HousePropertyCreateSerializer
        return HousePropertySerializer

    def get_permissions(self):
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request_user = DefaultUser.objects.get(user=request.user)
        address_data = request.data['address']
        address = Address.objects.get_or_create(
            city=address_data['city'],
            district=address_data['district'],
            street=address_data['street'],
            street_number=address_data['street_number'])[0]

        request.data['user'] = request_user.id
        request.data['address'] = model_to_dict(address)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            request_user = DefaultUser.objects.get(user=request.user)
            prop = HouseProperty.objects.get(id=pk)
            request.data['user'] = request_user.id

            if (prop.user.id != request_user.id):
                return Response({'error': 'You are not allowed to update this post.'}, status=status.HTTP_401_UNAUTHORIZED)

        except (DefaultUser.DoesNotExist, HouseProperty.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            request_user = DefaultUser.objects.get(user=request.user)
            prop = HouseProperty.objects.get(id=pk)

            if (prop.user.id != request_user.id):
                return Response({'error': 'You are not allowed to delete this post.'}, status=status.HTTP_401_UNAUTHORIZED)

        except (DefaultUser.DoesNotExist, HouseProperty.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().delete(request, *args, **kwargs)


class FlatPropertyViewSet(viewsets.ModelViewSet):
    queryset = FlatProperty.objects.all()
    serializer_class = FlatPropertySerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return FlatPropertyCreateSerializer
        return FlatPropertySerializer

    def get_permissions(self):
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request_user = DefaultUser.objects.get(user=request.user)
        address_data = request.data['address']
        address = Address.objects.get_or_create(
            city=address_data['city'],
            district=address_data['district'],
            street=address_data['street'],
            street_number=address_data['street_number'])[0]

        request.data['user'] = request_user.id
        request.data['address'] = model_to_dict(address)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            request_user = DefaultUser.objects.get(user=request.user)
            prop = FlatProperty.objects.get(id=pk)
            request.data['user'] = request_user.id

            if (prop.user.id != request_user.id):
                return Response({'error': 'You are not allowed to update this post.'}, status=status.HTTP_401_UNAUTHORIZED)

        except (DefaultUser.DoesNotExist, FlatProperty.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print('delete this post')
        try:
            request_user = DefaultUser.objects.get(user=request.user)
            prop = FlatProperty.objects.get(id=pk)

            if (prop.user.id != request_user.id):
                return Response({'error': 'You are not allowed to delete this post.'}, status=status.HTTP_401_UNAUTHORIZED)

        except (DefaultUser.DoesNotExist, FlatProperty.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().delete(request, *args, **kwargs)
