import sys
import random
from django.core.mail import send_mail
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from apps.authentication.models import User, PasswordReset, UserPermissions
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class CreateUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "role",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone",
        )
        write_only_fields = ("password",)
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            address=validated_data["address"],
            phone=validated_data["phone"],
            otp=random.randint(1111, 9999),
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        pass_reset = PasswordReset()
        pass_reset.user = user
        pass_reset.save()
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("This field must be unique.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("This field must be unique.")
        return value


class UserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissions
        fields = "__all__"


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone",
        )

    read_only_fields = ("id",)


class SupervisorDetailSerializer(serializers.ModelSerializer):
    supervisor_user = UserPermissionsSerializer(required=False, many=True)
    supervisor_user = serializers.SerializerMethodField("permission")

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone",
            "supervisor_user",
        )
        read_only_fields = ("id",)

    def permission(self, obj):
        permission = UserPermissions.objects.filter(supervisor_user=obj)
        return UserPermissionsSerializer(permission, many=True).data



class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class ForgetPasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for forget password endpoint.
    """

    email = serializers.CharField(required=True, max_length=100)
    otp = serializers.CharField(required=True, max_length=4)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "otp", "password"]

    def update(self, instance, validated_data):
        if instance.otp == validated_data["otp"]:
            instance.is_active = True
            instance.set_password(validated_data["password"])
            instance.save()
        else:
            raise serializers.ValidationError("Enter Valid otp")
        return instance


class LoginAuthSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "token")
        extra_kwargs = {
            "email": {
                "required": True,
                "error_messages": {"required": "Please fill this email field",},
            },
            "password": {
                "required": True,
                "error_messages": {"required": "Please fill this password field",},
            },
        }

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }
