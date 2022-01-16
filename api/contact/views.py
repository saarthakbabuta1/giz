from email import message
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .mail import send_mail
import json
# Create your views here.

class ContactView(viewsets.ViewSet):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny,]

    def list(self,request):
        queryset = Contact.objects.all()
        serializer = ContactSerializer(queryset,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        try:
            data = request.data
            serializer = ContactSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                data = request.data
                sender = "project.pvport@gmail.com"
                destination = "project.pvport@gmail.com"
                mail = send_mail(destination,sender,data["name"],data["mobile"],data["email"],data["message"])
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("Error Here,",e)
            return "Error Here: ",e