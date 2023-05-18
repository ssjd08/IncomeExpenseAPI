from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6 , write_only=True) #write_only=True means not passable to frontend.  # noqa: E501

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')  # noqa: F841
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('the username should only contain alphabetic characters')  # noqa: E501

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField() #automaticly search for get_tokens method in class.

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('invalid information, please try again.')

        if not user.is_active:
            raise AuthenticationFailed("Account is not active. contact administrator.")

        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified.")

        return {
            'email': user.email,
            'username': user.username,
            'token': user.tokens,
        }
        

class RestPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    
    class Meta:
        feilds = ['email']
        

class SETNewPasswordSerialize(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    
    class Meta:
        fields = ['password', 'token', 'uidb64']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64') 
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('the rest link is invalid', 401)
            user.set_password(password)        
            user.save()
            
        except Exception as e:
            raise AuthenticationFailed('the rest link is invalid',401)
        
        return super().validate(attrs)