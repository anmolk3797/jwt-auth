import json
import requests
import random
import uuid
from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from apps.authentication.models import User, PasswordReset, UserPermissions
from django.utils.dateparse import parse_date
from django.db.models import signals
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum, FloatField, Avg
from rest_framework.mixins import *
from rest_framework import generics, permissions, serializers
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import (
    CreateUserSerializer,
    ChangePasswordSerializer,
    ForgetPasswordSerializer,
    CreateUserSerializer,
    UserPermissionsSerializer,
    UpdateUserSerializer,
    LoginAuthSerializer ,
)

from django.conf import settings
from datetime import timedelta


class Register(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Created successfully"})
        else:
            pass
        return Response(serializer.errors)



class ResendOtpView(APIView):
    permission_classes = []

    def post(self, request):
        instance = get_object_or_404(User, email=request.data["email"])
        if instance.is_active == True:
            return Response({"message": "Already Verified"})
        else:
            send_mail(
                "CEP Email verification",
                "Your verification Code " + str(user.otp),
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Already sent"})


class Token(ObtainAuthToken, GenericAPIView):
    permission_classes = []
    serializer_class = LoginAuthSerializer

    def post(self, request):
        """
        Gets tokens with username and password. Input should be in the format:
        {"username": "username", "password": "1234abcd"}
        """
        username = request.data["username"]
        try:
            user = User.objects.get(username=username)
            if user.is_active == False:
                return Response({"message": "User is not active, please verify email."})
            else:
                pass
        except:
            email = User.objects.get(email=request.data["email"])
            if user.is_active == False:
                return Response({"message": "Bad request or Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                pass


        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


@receiver(signals.pre_save, sender=User)
def revoke_tokens(sender, instance, **kwargs):
    existing_user = User.objects.get(pk=instance.pk)

    if getattr(settings, 'REST_USE_JWT', False):
        if instance.password != existing_user.password:
            # If user has changed his password, generate manually a new token for him
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(instance)
            payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())
            instance.token = jwt_encode_handler(payload)


class UpdateProfileView(RetrieveAPIView, ListAPIView, UpdateModelMixin):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UpdateUserSerializer


    def get_object(self):
        obj = get_object_or_404(User, id=self.request.user.id)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ChangePasswordView(UpdateAPIView):
    """
        An endpoint for changing password.
        """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = User
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_object_or_404(User, email=request.GET.get("email", None))
        queryset = PasswordReset.objects.filter(user=user)
        if queryset.exists():
            password_reset = PasswordReset.first()
            # checking for last password reset
            if password_reset.timestamp < timezone.now() - timedelta(days=1):
                # password is not recently updated
                password_reset.delete()
                password_reset = PasswordReset(
                    user=user,
                    key="".join(
                        [choice("!@$_-qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890") for i in range(99)]
                    ),
                )
                password_reset.save()

                # send email here

                message = """To reset your password, go to localhost:8000/password_reset/{}""".format(password_reset.key)
                send_mail(
                    "Password reset request",
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                    )
                return Response({"message": "Email sent"})
            else:
                pass
                # recent password updated
                return Response({"error": "Your password was updated recently, wait before updating it again."})


    def post(self, request):
        instance = get_object_or_404(User, email=request.data["email"])

        queryset = PasswordReset.objects.filter(key=request.POST.get("key"))
        if queryset.exists():
            password_reset = queryset.first()

            if password_reset.timestamp < timezone.now() - timedelta(minutes=30):
                # expired
                return Response({"error": "Password reset key is expired! Try fresh after some hours."})

            else:
                # valid
                password = request.POST.get("password", "")
                if password == "":
                    # valid key and waiting for password
                    return Response({"success": "Set a new password"})

                else:
                    # seting up the password
                    user = password_reset.user
                    user.set_password(password)
                    user.save()
                    return Response({"success": "Password updated successfully."})

        else:
            # invalid key
            return Response({"error": "Invalid key"})

