from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        
    def validate(self, attrs):
        email = attrs.get('email','') #get data from request.
        username = attrs.get('username','')
        
        if not username.isalnum(): #does not allow spaces in username.
            raise serializers.ValidationError(
                "The username should be alphabetic characters")
            
        return attrs
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)