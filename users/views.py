from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response 
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view
from .models import User
from . import serializers 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
)

# Create your views here.
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID del usuario", type=openapi.TYPE_INTEGER),
        openapi.Parameter('email', openapi.IN_QUERY, description="Correo electrónico del usuario", type=openapi.TYPE_STRING),
    ],
)
@api_view(['GET'])
def userCRUD(request):
    #Search one User by ID or Email
    if request.method == 'GET': 
        user_id = request.query_params.get('id')
        email = request.query_params.get('email')
        if not user_id == None:
            if not int(user_id) > 0 or int(user_id) > 1000:
                return Response({"error": "Sorry, ID is out of limit"}, status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            user_id = 0
        if not email == None:    
            if len(email) > 100 or len(email) < 5:
                return Response({"error": "Sorry, EMAIL is out of limit"}, status=status.HTTP_412_PRECONDITION_FAILED)
        #queryset
        try:
            user = User.objects.get(Q(email=email) | Q(id=int(user_id))) #Email or ID
        except ObjectDoesNotExist:
            return Response({"error": "Sorry, this User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        #serializer
        serializer_class = serializers.BasicUserSerializer(user, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
        

class CreateUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        user = serializer.save()

        return Response({
            "user": serializers.BasicUserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully!"
        })


class UpdateUserView(RetrieveUpdateAPIView):
    serializer_class = serializers.UpdateUserSerializer
    def get_queryset(self):
        return User.objects.all()
    

class DeleteUserView(RetrieveDestroyAPIView):
    serializer_class = serializers.DeleteUserSerializer
    queryset = User.objects.all()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if check_password(request.data.get('password1'), instance.password):
            instance.delete()
            return Response({"message": "the user was deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'invalid password'}, status=status.HTTP_412_PRECONDITION_FAILED)
    
    
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = serializers.CustomAuthTokenSerializer
