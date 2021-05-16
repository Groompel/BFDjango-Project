from django.http.response import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from misc.serializers import BusinessCenterSerializer, ResidentialComplexSerializer
from misc.models import BusinessCenter, ResidentialComplex
from django.shortcuts import render
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)

# Create your views here.


class ResidentialComplexesList(APIView):

    def get(self, request):
        complexes = ResidentialComplex.objects.all()

        ser = ResidentialComplexSerializer(complexes, many=True)

        logger.info('List all residential complexes')

        return Response(ser.data)

    def post(self, request):
        ser = ResidentialComplexSerializer(data=request.data)

        if ser.is_valid():
            ser.save()

            return Response(ser.data, status.HTTP_201_CREATED)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)


class ResidentialComplexDetail(APIView):

    def get_permissions(self):
        permission_classes = []
        if self.request.method in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [
                permissions.IsAuthenticated, permissions.IsAdminUser]
        elif self.request.method in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_object(self, id):
        try:
            return ResidentialComplex.objects.get(id=id)
        except ResidentialComplex.DoesNotExist:
            raise Http404

    def get(self, request, id):
        rc = self.get_object(id)

        ser = ResidentialComplexSerializer(rc)

        logger.info('Get residential complex detail. ID: %s' % id)

        return Response(ser.data)

    def put(self, request, id):
        rc = self.get_object(id)

        ser = ResidentialComplexSerializer(rc, request.data)

        if ser.is_valid():
            ser.save()

            return Response(ser.data)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        rc = self.get_object(id)

        rc.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BusinessCentersList(APIView):

    def get(self, request):
        centers = BusinessCenter.objects.all()

        ser = BusinessCenterSerializer(centers, many=True)

        logger.info('List all business centers')

        return Response(ser.data)

    def post(self, request):
        ser = BusinessCenterSerializer(data=request.data)

        if ser.is_valid():
            ser.save()

            return Response(ser.data, status.HTTP_201_CREATED)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)


class BusinessCenterDetail(APIView):

    def get_permissions(self):
        permission_classes = []
        if self.request.method in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [
                permissions.IsAuthenticated, permissions.IsAdminUser]
        elif self.request.method in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_object(self, id):
        try:
            return BusinessCenter.objects.get(id=id)
        except BusinessCenter.DoesNotExist:
            raise Http404

    def get(self, request, id):
        bc = self.get_object(id)

        ser = BusinessCenterSerializer(bc)

        logger.info('Get business center detail. ID: %s' % id)

        return Response(ser.data)

    def put(self, request, id):
        bc = self.get_object(id)

        ser = BusinessCenterSerializer(bc, request.data)

        if ser.is_valid():
            ser.save()

            return Response(ser.data)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        bc = self.get_object(id)

        bc.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
