from django.shortcuts import render
from rest_framework import viewsets, permissions
from properties.models import CommercialProperty, FlatProperty, HouseProperty
from properties.serializers import CommercialPropertySerializer, FlatPropertySerializer, HousePropertySerializer

# Create your views here.


class CommercialProperyViewSet(viewsets.ModelViewSet):
    queryset = CommercialProperty.objects.all()
    serializer_class = CommercialPropertySerializer
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]


class HousePropertyViewSet(viewsets.ModelViewSet):
    queryset = HouseProperty.objects.all()
    serializer_class = HousePropertySerializer
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]


class FlatPropertyViewSet(viewsets.ModelViewSet):
    queryset = FlatProperty.objects.all()
    serializer_class = FlatPropertySerializer
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]
