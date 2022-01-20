from rest_framework.relations import ManyRelatedField
from .models import Models,Products
from django.utils.text import gettext_lazy as _
from rest_framework import serializers


class PvModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Models
        fields = ("sku","name","description","brand","grid","components")

class PvProductsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ("sku","oem","assembly","comments","quantity","available_quantity")