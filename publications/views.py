from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.response import Response 
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Publication
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
from users.serializers import MinimalUserSerializer
from users.models import User
 
#pagination
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
    

class PublicationRetrieveView(RetrieveAPIView):
    queryset = Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    lookup_field = 'pk'
    
class CreatePublicationView(CreateAPIView):
    serializer_class = serializers.CreatePublicationSerializer
    queryset = Publication.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(Q(email=serializer.validated_data.get('user')) | Q(id=serializer.validated_data.get('user.id')))
        publication = serializer.save()
        return Response({
            "publication": serializers.CreatePublicationSerializer(publication, context=self.get_serializer_context()).data,
            "user_data": MinimalUserSerializer(user).data,
            "message": "Publication created successfully!"
        }, status=status.HTTP_201_CREATED)
    
class UpdatePublicationView(RetrieveUpdateAPIView):
    serializer_class = serializers.CreatePublicationSerializer
    def get_queryset(self):
        return Publication.objects.all()
    
class DeletePublicationView(RetrieveDestroyAPIView):
    serializer_class = serializers.DeletePublicationSerializer
    queryset = Publication.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.multimedia: 
            usuario = instance.user
            nombre_archivo = 'publications/' + usuario.email + '/' + instance.multimedia.split('/')[-1]
            # Elimina el archivo del bucket
            blob = serializers.bucket.blob(nombre_archivo)
            blob.delete()
            instance.delete()
            return Response({"message": "the publication was deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            instance.delete()
            return Response({"message": "the publication was deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class EntertainmentPublicationListView(ListAPIView):
    serializer_class = serializers.PublicationSerializer
    queryset = Publication.objects.filter(category='Entretenimiento')
    pagination_class = LargeResultsSetPagination

class DevelopmentPublicationListView(ListAPIView):
    serializer_class = serializers.PublicationSerializer
    queryset = Publication.objects.filter(category='Innovación')
    pagination_class = LargeResultsSetPagination

    