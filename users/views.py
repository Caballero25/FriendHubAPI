from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view
from .models import User
from .serializers import BasicUserSerializer

# Create your views here.
#authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def userCRUD(request, *args, **kwargs):
    if request.method == 'GET': #Search one User by ID or Email
        user_id = request.data.get('id')
        email = request.data.get('email')
        if not user_id == None:
            if not user_id > 0 or user_id > 1000:
                return Response({"error": "Sorry, ID is out of limit"}, status=status.HTTP_412_PRECONDITION_FAILED)
        if not email == None:    
            if len(email) > 100 or len(email) < 5:
                return Response({"error": "Sorry, EMAIL is out of limit"}, status=status.HTTP_412_PRECONDITION_FAILED)
        #queryset
        try:
            user = User.objects.get(Q(email=email) | Q(id=user_id)) #Email or ID
        except ObjectDoesNotExist:
            return Response({"error": "Sorry, this User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        #serializer
        serializer_class = BasicUserSerializer(user, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'POST':
        #data
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        #queryset
        user = User.objects.filter(email=email).first()
        if user:
            return Response({"error":"User already exist"}, status=status.HTTP_409_CONFLICT)
        else:
            new_user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
            new_user.set_password(password)
            new_user.save()
            #serializer
            serializer_class = BasicUserSerializer(new_user, many=False)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)


