from django.core.validators import validate_email as django_validate_email
from django.contrib.auth import get_user_model
from rest_framework import serializers, pagination
from google.api_core.exceptions import NotFound, Forbidden
from .models import User
from google.cloud import storage
import re
import json


# Read secret.json
with open('secret.json') as f:
    secret_data = json.load(f)

#Images storage
client = storage.Client.from_service_account_json('./friendshub-firebase.json')
bucket = client.get_bucket(secret_data['bucket'])



class BasicUserSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User 
        fields = ('id', 'first_name', 'last_name', 'email', 'avatar',
                  'banner', 'biography', 'birthdate', 'location', 'create_at',
                  'friends')  
        def validate_email(self, value):
            try:
                django_validate_email(value)
            except:
                raise serializers.ValidationError("Email is not valid")
            return value
        
    def get_friends(self, obj):
        try:
            friends_list = [{'id': friend.id, 'first_name': friend.first_name, 'last_name': friend.last_name} for friend in obj.friends.all()]
            return friends_list
        except:
            return []

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):      
        if len(data['password1']) < 4:
            raise serializers.ValidationError("password must be at least 4 characters")
        elif data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name =validated_data['last_name']
        )   
        user.set_password(validated_data['password1'])
        user.save()
        return user    



class UpdateUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    banner = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'avatar',
                  'banner', 'biography', 'birthdate', 'location') 
    
    def validated_avatar(self, value):
        return value
    def validated_banner(self, value):
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Obtener la URL de la imagen desde el campo avatar y agregarla a la representación
        if instance.avatar or instance.banner:
            representation['avatar'] = instance.avatar
            representation['banner'] = instance.banner
        return representation

    def update(self, instance, validated_data):
        avatar_file = validated_data.get('avatar')  # Obtén el archivo de imagen del validated_data
        banner_file = validated_data.get('banner')  # Obtén el archivo de imagen del validated_data
        if avatar_file:
            print(2)
            # Nombre del archivo en Firebase Storage
            filename = 'avatars/{}/{}'.format(instance.email, avatar_file.name)
            
            # Subir la imagen a Firebase Storage
            blob = bucket.blob(filename)
            blob.upload_from_file(avatar_file, content_type=avatar_file.content_type)
            blob.make_public()

            # Obtener la URL de la imagen subida
            image_url = blob.public_url

            # Asignar la URL de la imagen a user_avatar
            instance.avatar = image_url
            instance.save()  # Guardar la instancia actualizada
        elif banner_file:
            print(2)
            # Nombre del archivo en Firebase Storage
            filename = 'banners/{}/{}'.format(instance.email, banner_file.name)
            
            # Subir la imagen a Firebase Storage
            blob = bucket.blob(filename)
            blob.upload_from_file(banner_file, content_type=banner_file.content_type)
            blob.make_public()

            # Obtener la URL de la imagen subida
            image_url = blob.public_url

            # Asignar la URL de la imagen a user_avatar
            instance.banner = image_url
            instance.save()  # Guardar la instancia actualizada
            
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.biography = validated_data.get('biography', instance.biography)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.location = validated_data.get('location', instance.location)

        instance.save()  # Guardar la instancia actualizada
        return instance


class DeleteUserSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 and password2 and password1 == password2:
            return data
        else:
            raise serializers.ValidationError("Passwords do not match.")
        


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = get_user_model().objects.filter(email=email).first()

            if user:
                if user.check_password(password):
                    if not user.is_active:
                        raise serializers.ValidationError('User account is disabled.')
                else:
                    raise serializers.ValidationError('Incorrect password.')
            else:
                raise serializers.ValidationError('User not found.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs
    