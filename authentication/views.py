from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, RestPasswordEmailRequestSerializer, SETNewPasswordSerialize
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .rendereres import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util



# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token # gives us two token for access and refresh token. we use access token.
        current_site = get_current_site(request).domain
        relative_link = reverse('verify_email') # takes url from name of page.
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = "hi "+user.username+" Use link below for verify your email\n" + absurl
        data = {
            'email_body':email_body,
            'email_subject': 'Verify your email',
            'to_email': user.email
        }
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description' , type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token', None)
        if token is None:
            return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully activated.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token is invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RestPasswordEmailRequestSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email','')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user) #for making a token one time useable.
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token}) # takes url from name of page.
            absurl = 'http://'+current_site+relative_link
            email_body = "hi \n Use link below to reset your password on income expence site\n" + absurl
            data = {
                    'email_body':email_body,
                    'email_subject': 'Reset your Password',
                    'to_email': user.email
            }
            Util.send_email(data)

        return Response({'success': "we have sent you a link to your email for change password"}, status=status.HTTP_200_OK)
        
        
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SETNewPasswordSerialize
    
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64)) #?
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is invalid, please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success': True, 'massage': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
            
        except DjangoUnicodeDecodeError as identifier :
            return Response({'error':'Token is invalid, please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class SetNewPasswordAPIVeiw(generics.GenericAPIView):
    serializer_class = SETNewPasswordSerialize
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'massage': 'Password Reset sucsses!'})
        