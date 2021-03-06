from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
import jwt
import json

from .serializers import UserSerializer
from coconut_server.settings import SECRET_KEY

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
@permission_classes((AllowAny, ))
class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    model = User
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            user = self.model.objects.get(username=serializer.data['username'])
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            auth_obj = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            print(auth_obj)
            if auth_obj:
                auth.login(request, auth_obj)
            return Response(
                token,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

@permission_classes((AllowAny, ))
class LoginUserView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, SECRET_KEY)
            return Response( token,
                status=status.HTTP_200_OK,
                )
        else:
            return Response(
              {'error': 'Invalid credentials',
              'status': 'failed'},
              status=status.HTTP_400_BAD_REQUEST
            )
