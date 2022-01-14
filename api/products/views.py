from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from .models import Models, Products
from .serializers import PvModelsSerializer,PvProductsSerializers
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated

# Create your views here.

class PvModel(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def list(self,request):
        queryset = Models.objects.all()
        serializer = PvModelsSerializer(queryset,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def retrieve(self, request, pk=None):
        queryset = Models.objects.all()
        model = get_object_or_404(queryset, pk=pk)
        serializer = PvModelsSerializer(model)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = PvModelsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
     
    def put(self,request,pk=None):
        queryset = Models.objects.all()
        model = get_object_or_404(queryset,pk=pk)
        serializer = PvModelsSerializer(model,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk=None):
        queryset = Models.objects.all()
        model = get_object_or_404(queryset,pk=pk)
        model.delete()
        return Response("{} model has been deleted".format(pk),status=status.HTTP_200_OK)


class PvModelList(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def list(self, request, pk=None):
        queryset = Models.objects.all()
        model = get_object_or_404(queryset, pk=pk)
        serializer = PvModelsSerializer(model)
        return Response(serializer.data,status=status.HTTP_200_OK)



class PvProduct(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def list(self,request):
        queryset = Products.objects.all()
        serializer = PvProductsSerializers(queryset,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def retrieve(self, request, pk=None):
        queryset = Products.objects.all()
        model = get_object_or_404(queryset, pk=pk)
        serializer = PvProductsSerializers(model)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = PvProductsSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
     
    def put(self,request,pk=None):
        queryset = Products.objects.all()
        model = get_object_or_404(queryset,pk=pk)
        serializer = PvProductsSerializers(model,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk=None):
        queryset = Products.objects.all()
        model = get_object_or_404(queryset,pk=pk)
        model.delete()
        return Response("{} model has been deleted".format(pk),status=status.HTTP_200_OK)

class PvProductList(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def get(self, request, pk=None):
        queryset = Products.objects.all()
        model = get_object_or_404(queryset, pk=pk)
        serializer = PvProductsSerializers(model)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ModuleProductList(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def list(self,request,pk=None):
        queryset = Products.objects.filter(sku_model=pk)
        serializer = PvProductsSerializers(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
