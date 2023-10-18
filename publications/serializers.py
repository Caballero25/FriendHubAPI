from django.core.validators import validate_email as django_validate_email
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Publication, Reaction, Comment, Category
from users.models import User
from users import serializers as UserSerializers
from rest_framework.authtoken.models import Token
from google.cloud import storage
#from . import friendshub_firebase 
import os
from dotenv import load_dotenv

#Images storage
load_dotenv()
client = storage.Client.from_service_account_json("friendshub-8a039-firebase-adminsdk-amwfa-bf38ccca17.json")
bucket = client.get_bucket(os.environ.get("BUCKET"))
categorys = ['Entretenimiento', 'Innovación']

class CreatePublicationSerializer(serializers.ModelSerializer):
    multimedia = serializers.FileField(required=False)
    class Meta:
        model = Publication
        fields = '__all__'

    def validated_multimedia(self, value):
        return value
    
    def validated_user(self, value):
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Obtener la URL de la imagen desde el campo avatar y agregarla a la representación
        if instance.multimedia:
            representation['multimedia'] = instance.multimedia
        return representation
    
    def validate(self, data):
        body = data.get('body')
        multimedia = data.get('multimedia')
        gif = data.get('gif')
        category = data.get('category')
        if not body and not multimedia and not gif:
            raise serializers.ValidationError("Debe proporcionar al menos un contenido (body, multimedia o gif).")
        if category not in categorys:
            raise serializers.ValidationError("Categoría no válida. Esperado: (Entretenimiento o Innovación)")
        return data
    
    def create(self, validated_data):
        multimedia_file = validated_data.get('multimedia')  # Obtén el archivo de imagen del validated_data
        user = User.objects.get(Q(email=validated_data.get('user')) | Q(id=validated_data.get('user.id')))
        if multimedia_file:
            # Nombre del archivo en Firebase Storage
            filename = 'publications/{}/{}'.format(user.email, multimedia_file.name)
            # Subir la imagen a Firebase Storage
            blob = bucket.blob(filename)
            blob.upload_from_file(multimedia_file, content_type=multimedia_file.content_type)
            blob.make_public()
            # Obtener la URL de la imagen subida
            image_url = blob.public_url
        else:
            image_url = None
        publication = Publication(
            user = user, 
            body = validated_data['body'],
            multimedia = image_url,
            gif = validated_data['gif'],
            category = validated_data['category']
        )
        publication.save()
        return publication
    
    def update(self, instance, validated_data):
        multimedia_file = validated_data.get('multimedia')  # Obtén el archivo de imagen del validated_data
        user = User.objects.get(Q(email=validated_data.get('user')) | Q(id=validated_data.get('user.id')))
        if multimedia_file:
            # Nombre del archivo en Firebase Storage
            filename = 'publications/{}/{}'.format(user.email, multimedia_file.name)
            
            # Subir la imagen a Firebase Storage
            blob = bucket.blob(filename)
            blob.upload_from_file(multimedia_file, content_type=multimedia_file.content_type)
            blob.make_public()

            # Obtener la URL de la imagen subida
            image_url = blob.public_url

            # Asignar la URL de la imagen a user_avatar
            instance.multimedia = image_url
            instance.save()  # Guardar la instancia actualizada
        instance.body = validated_data.get('body', instance.body)
        instance.gif = validated_data.get('gif', instance.gif)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

class DeletePublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    user = UserSerializers.MinimalUserSerializer()
    class Meta:
        model = Publication
        fields = '__all__'