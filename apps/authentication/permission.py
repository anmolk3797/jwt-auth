from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import exceptions
from users.models import User, UserPermissions
from django.urls import resolve
import uuid


class TokenHasScopeForMethod(TokenHasScope):
    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        if hasattr(token, "scope"):
            if request.auth.scope == "club_owner":
                # Get the scopes required for the current method from the view
                # required_scopes = view.required_scopes_per_method[request.method]
                # required_scopes = view.request.method
                current_url = resolve(request.path_info)
                user_id = request.user
                check = False
                user = User.objects.get(id=user_id.id)
                permission = UserPermissions.objects.get(supervisor_user=user_id)

                if check == True:
                    return bool(request.user and request.user.is_authenticated)
                else:
                    return False
            elif request.auth.scope == "superuser":
                # return token.is_valid(required_scopes)
                return bool(request.user and request.user.is_authenticated)
            else:
                pass
