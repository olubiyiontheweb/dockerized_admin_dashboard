#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions, viewsets
from .models import User, Permission, Role
from .serializers import UserSerializer, RoleSerializer
from .authentication import generate_access_token, jwtAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# These are API views for user registration and authentication 

#API end point for user registration
@api_view(['POST'])
def register(request):
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

# API endpoint for login
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password!')

    response = Response('success')

    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)

    response.data = {
        'jwt':token
    }

    return response

@api_view(['POST'])
def logout(request):

    response = Response()
    response.delete_cookie(key='jwt')

    response.data = {
        'message': 'Logout Successful'
    }


# get user from submited jwt token during login
class AuthenticatedUser(APIView):

    authentication_classes = [jwtAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response({
            'data': serializer.data
        })

class PermissionAPIView(APIView):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })

class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)

        return Response({
            'data':serializer.data
        })

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


# @api_view(['GET'])
# def users(request):
#     users = User.objects.all()

#     serializer = UserSerializer(users, many=True)

#     return  Response(serializer.data)