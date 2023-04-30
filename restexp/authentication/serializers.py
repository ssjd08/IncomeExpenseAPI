from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6 , write_only=True)#write_only=True means not passable to frontend.
    
    class Meta:
        model = User['username', 'email', 'password']