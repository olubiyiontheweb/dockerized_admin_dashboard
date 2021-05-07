from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from dashboard.pagination import CustomPagination
from users.authentication import jwtAuthentication
from .serializers import ProductSerializer
from .models import Product


# Create your views here.
class ProductGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    authentication_classes = [jwtAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = CustomPagination

    def get(self, request, pk = None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

    def post(self, request):
        return Response({
            'data': self.create(request, pk).data
        })

    def put(self, request, pk=None):
        return Response({
            'data': self.partial_update(request, pk).data
        })
    
    def delete(self, request, pk=None):
        return self.destroy(request, pk)
