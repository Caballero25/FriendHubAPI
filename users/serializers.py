from django.core.validators import validate_email as django_validate_email
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