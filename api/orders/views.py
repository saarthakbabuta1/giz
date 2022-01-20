from django.shortcuts import render

from rest_framework import viewsets
from .serializers import OrdersSerializers
from .models import OrdersModel
from products.models import Products
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime

# Create your views here.

class OrdersViews(viewsets.ViewSet):
    serializer = OrdersSerializers()
    def post(self,request):
        data = request.data
        data['created_date'] = datetime.now()
        data['last_updated'] = datetime.now()
        serializer = OrdersSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def get(self,request):
        queryset = OrdersModel.objects.all()
        serializer = OrdersSerializers(queryset,many = True)
        resp = serializer.data
        for i in resp:
            prod = {}
            for j in i['products'].keys():
                prod[j] =  list(Products.objects.filter(sku=j).values())[0]
                prod[j]["quantity"] = i["products"][j]
            i['products'] = prod
        return Response(resp,status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = OrdersModel.objects.all()
        model = get_object_or_404(queryset, id=pk)
        serializer = OrdersSerializers(model)
        resp = serializer.data

        # prod = {}
        # for j in resp['products'].keys():
        #     prod[j] =  list(Products.objects.filter(sku=j).values())[0]
        #     prod[j]["quantity"] = resp["products"][j]
        # resp['products'] = prod

        return Response(resp,status=status.HTTP_200_OK)

    def put(self,request,pk=None):
        queryset = OrdersModel.objects.all()
        model = get_object_or_404(queryset,id=pk)
        data = request.data
        data['last_updated'] = datetime.now()
        serializer = OrdersSerializers(model,data=data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class CancelOderView(viewsets.ViewSet):
    serializer = OrdersSerializers

    def put(self,request,pk=None):
        queryset = OrdersModel.objects.all()
        model = get_object_or_404(queryset,id=pk)
        data = request.data
        data['last_updated'] = datetime.now()
        data['order_status'] = "Cancelled"
        serializer = OrdersSerializers(model,data=data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)