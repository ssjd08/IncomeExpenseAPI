from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User 
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

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
        } 
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass 