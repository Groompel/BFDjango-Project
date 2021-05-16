from django.http.response import Http404
from rest_framework import response
from rest_framework import permissions
from rest_framework.views import APIView
from _auth.models import Agency, Agent, DefaultUser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from _auth.serializers import AgencySerializer, AgentSerializer, DefaultUserCreateSerializer, DefaultUserSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
import logging

logger = logging.getLogger(__name__)

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    ser = DefaultUserCreateSerializer(data=request.data)

    if ser.is_valid():
        un = request.data['username']
        try:
            DefaultUser.objects.get(user__username=un)
            return Response({'error': 'The username "%s" is already taken' % un}, status.HTTP_400_BAD_REQUEST)

        except DefaultUser.DoesNotExist:
            ser.save()
            logger.info('New user has been registered %s' % un)
            return Response(ser.data, status.HTTP_201_CREATED)

    return Response(ser.errors, status.HTTP_400_BAD_REQUEST)


def get_user_and_check(request_user):
    try:

        user = DefaultUser.objects.get(user=request_user)

        # if (request_user != user):
        #     return Response({'error': 'You don\'t have permission to access this user.'}, status.HTTP_401_UNAUTHORIZED)

        return user
    except DefaultUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = get_user_and_check(request.user)
    if (request.method == 'GET'):
        ser = DefaultUserSerializer(user)
        logger.info('Retieve a user profile of %s' % user.user.username)
        return Response(ser.data)
    elif (request.method == 'PUT'):
        ser = DefaultUserSerializer(user, request.data)
        if ser.is_valid():
            ser.save()
            logger.info('Edit profile of %s' % user.user.username)
            return Response(ser.data)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)
    elif (request.method == 'DELETE'):
        user.user.delete()
        user.delete()
        logger.info('Delete profile of %s' % user.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListAgencies(APIView):

    def get_permissions(self):
        permission_classes = []
        if self.request.method in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.request.method in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get(self, request):
        agencies = Agency.objects.all()

        ser = AgencySerializer(agencies, many=True)

        logger.info('List all of the agencies')
        return Response(ser.data)

    def post(self, request):
        user_id = DefaultUser.objects.get(user=request.user).id

        data = request.data.dict()
        data.update({'owner': user_id})
        print(data)
        ser = AgencySerializer(data=data)
        if ser.is_valid():
            ser.save()
            logger.info('Create new agency `%s`' % data['name'])

            return Response(ser.data, status.HTTP_201_CREATED)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)


class AgencyDetails(APIView):

    def get_permissions(self):
        permission_classes = []
        if self.request.method in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.request.method in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_object(self, id):
        try:
            return Agency.objects.get(id=id)
        except Agency.DoesNotExist:
            raise Http404

    def get(self, request, id):
        agency = self.get_object(id)

        ser = AgencySerializer(agency)

        logger.info('Get agency %s' % ser.data['name'])
        return Response(ser.data)

    def put(self, request, id):
        agency = self.get_object(id)
        user = DefaultUser.objects.get(user=request.user)

        if agency.owner != user:
            logger.error('Not authorized to update the agency `%s` by user %s' % (
                agency.name, user.user.username))
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        ser = AgencySerializer(agency, data=request.data)

        if ser.is_valid():
            ser.save()
            logger.info('Update agency `%s`' % ser.data['name'])
            return Response(ser.data)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        agency = self.get_object(id)

        user = DefaultUser.objects.get(user=request.user)

        if agency.owner != user:
            logger.error('Not authorized to delete the agency `%s` by user %s' % (
                agency.name, user.user.username))
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        logger.info('Deleted agency `%s`' % agency.name)
        agency.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def become_agent(request):
    user = DefaultUser.objects.get(user=request.user)
    agency_id = request.data.get('agency', None)

    if (agency_id == None):
        return Response({'error': 'No agency was provided.'}, status.HTTP_400_BAD_REQUEST)
    elif (user.is_agent == True):
        return Response(status.HTTP_201_CREATED)

    user.is_agent = True
    try:
        agency = Agency.objects.get(id=agency_id)
    except Agency.DoesNotExist:
        return Response({'error': 'Agency with id %s does not exist' % agency_id})

    Agent.objects.get_or_create(user=user, agency=agency)
    user.save()
    logger.info('User %s has just became an agent' % user.user.username)

    ser = DefaultUserSerializer(user)

    return Response(ser.data, status.HTTP_201_CREATED)
