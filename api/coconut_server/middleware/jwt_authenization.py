# coding=utf-8
import jwt
import traceback

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser, User
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user

settings = LazySettings()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_user(request):

        user_jwt = get_user(request)
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if user_jwt and token is None:
            return user_jwt
        user_jwt = AnonymousUser()
        if token is not None:
            print(token)
            user_jwt = jwt.decode(
                token,
                settings.SECRET_KEY,
            )
            user_jwt = User.objects.get(
                id=user_jwt.get('user_id')
            )
            return user_jwt
            # print("user_jwt=>>>>>>>>>>>>>>>>", user_jwt)
            # except Exception as e: # NoQA
            #     traceback.print_exc()
        return user_jwt