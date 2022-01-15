from .models import Contact
from .serializers import ContactSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ContactView(viewsets.ViewSet):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny,]

    def list(self,request):
        queryset = Contact.objects.all()
        serializer = ContactSerializer(queryset,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ContactSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

