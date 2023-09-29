from rest_framework import serializers, pagination
from .models import User


class BasicUserSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User 
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'avatar',
                  'banner', 'biography', 'birthdate', 'location', 'create_at',
                  'friends')  
        
    def get_friends(self, obj):
        return [{'id': friend.id, 'first_name': friend.first_name, 'last_name': friend.last_name} for friend in obj.friends.all()]