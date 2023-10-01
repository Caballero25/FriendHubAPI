from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import BasicUserSerializer

# Create your views here.
#authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def userCRUD(request):
    #Search one User by ID or Email
    if request.method == 'GET': 
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
        
    #Create user
    elif request.method == 'POST':
        serializer_class = BasicUserSerializer(data = request.data, many=False)
        if serializer_class.is_valid():
            #data 
            email = request.data.get('email')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            password = request.data.get('password')
            if email == None or first_name == None or last_name == None or password == None:
                return Response({"error": {"Data not can be null": {"email": email,
                                                                    "first_name": first_name, #Nonetype data is not admissible
                                                                    "last_name": last_name,
                                                                    "password": password}}}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")
            #queryset
            user = User.objects.filter(email=email).first()
            if user:
                return Response({"error":"User already exist"}, status=status.HTTP_409_CONFLICT, content_type="application/json")
            else:
                new_user = User(email=email, first_name=first_name, last_name=last_name)
                new_user.set_password(password)
                new_user.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED, content_type="application/json")
        else:
            return Response(serializer_class.errors, status=status.HTTP_404_NOT_FOUND, content_type="application/json")

    #Edit user
    elif request.method == 'PUT':
        user_id = request.data.get('id')
        if user_id == None or not user_id > 0:
            return Response({"error": "ID invalid"}, status=status.HTTP_412_PRECONDITION_FAILED, content_type="application/json")
        try:
            edit_user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({"error": "Sorry, this User does not exist"}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")
        
        serializer_class = BasicUserSerializer(edit_user, data=request.data, partial=True)
        
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK, content_type="application/json")
        else:
            return Response(serializer_class.errors, status=status.HTTP_404_NOT_FOUND, content_type="application/json")
        
    #Delete user
    elif request.method == "DELETE":
        user_id = request.data.get('id')
        user_pw = request.data.get('password')
        if user_id == None or not user_id > 0:
            return Response({"error": "ID invalid"}, status=status.HTTP_412_PRECONDITION_FAILED, content_type="application/json")
        try:
            edit_user = User.objects.get(id=user_id)
            token_user = Token.objects.get(user=edit_user)
        except ObjectDoesNotExist:
            return Response({"error": "Sorry, this User does not exist"}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")
        password_matched = check_password(user_pw, edit_user.password)
        if password_matched: 
            edit_user.delete()
            token_user.delete()
            return Response({"message": "user has been deleted successfully"}, status=status.HTTP_200_OK)
        else: 
            return Response({"error": "passwords do not match"}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")
        
            
