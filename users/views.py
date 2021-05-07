#from django.shortcuts import render
from dashboard.pagination import CustomPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions, viewsets, status, generics, mixins
from .models import User, Permission, Role
from .serializers import UserSerializer, RoleSerializer
from .permissions import ViewPermissions
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

    permission_classes = [IsAuthenticated & ViewPermissions]

    def get(self, request):
        data = UserSerializer(request.user).data
        data['permissions'] = [p['name'] for p in data['role']['permissions']]
        serializer = UserSerializer(request.user)

        return Response({
            'data': serializer.data
        })

class PermissionAPIView(APIView):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })

class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'roles'

    def list(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)

        return Response({
            'data':serializer.data
        })

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data':serializer.data
        }, status= status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(role)

        return Response({
            'data': serializer.data
        })

    def update(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data':serializer.data
        }, status=status.HTTP_202_ACCEPTED)


    def destroy(self, request, pk=None):
        role = Role.objects.get(id=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def users(request):
#     users = User.objects.all()

#     serializer = UserSerializer(users, many=True)

#     return  Response(serializer.data)

class UserGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'users'

    queryset = User.objects.all()
    serializer_class = UserSerializer

    pagination_class = CustomPagination

    def get(self, request, pk = None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

    def post(self, request):
        request.data.update({
            'password': 1234
            #'role': request.data['role_id']
        })
        return Response({
            'data': self.create(request, pk).data
        })

    def put(self, request, pk=None):

        if request.data['role_id']:
            request.data.update({
                'role': request.data['role_id']
            })

        return Response({
            'data': self.partial_update(request, pk).data
        })
    
    def delete(self, request, pk=None):
        return self.destroy(request, pk)

class ProfileInfoAPIView(APIView):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'users'

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=true)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfilePasswordAPIView(APIView):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]

    def put(self, request, pk=None):
        user = request.user

        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('Passwords do not match')

        serializer = UserSerializer(user, data=request.data, partial=true)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)