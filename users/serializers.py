from django.core.validators import validate_email as django_validate_email
from django.contrib.auth import get_user_model
from rest_framework import serializers, pagination
from .models import User
import re


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

class PostUser(serializers.Serializer):
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



class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'avatar',
                  'banner', 'biography', 'birthdate', 'location') 
        

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
    