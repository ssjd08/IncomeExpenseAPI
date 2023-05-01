from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6 , write_only=True)#write_only=True means not passable to frontend.
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']\
            
    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','') 
        
        if not username.isalnum():
            raise serializers.ValidationError('the username should only contain alphabetic characters')
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)