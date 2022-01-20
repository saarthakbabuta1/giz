import imp
from rest_framework import serializers
from .models import OrdersModel
from datetime import datetime

class OrdersSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrdersModel
        fields = ("id","user","products","created_date",
        "last_updated","amount","order_status","delivery_location","discom",
        "ca_number","order_confirmation","delivery_timeline","tech_contact_information")

    