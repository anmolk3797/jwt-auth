from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
import uuid


class BaseModel(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at      = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created At"))
    modified_at     = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_("Modified At"))

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError("The username must be set")
        # username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, password, **extra_fields)


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username        = models.CharField(max_length=100, null=True, blank=True, unique=True)
    password        = models.CharField(max_length=30, null=True, blank=False, verbose_name=_("Password"))
    email           = models.EmailField(null=True, blank=False, verbose_name=_("Email"))
    first_name      = models.CharField(max_length=30, null=True, blank=False, verbose_name=_("First name"))
    last_name       = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Last name"))
    address         = models.CharField(max_length=254, null=True, blank=True, verbose_name=_("Address"))
    phone           = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Cell phone"))
    dob             = models.DateField(null=True, blank=True)
    gender          = models.CharField(max_length=10, null=True, blank=True)
    profile_picture = models.ImageField(null=True, max_length=255, upload_to="profile_pictures/%Y/%m/%d/", blank=True)
    otp             = models.CharField(max_length=4, null=True, blank=True, verbose_name=_("otp"))
    created_at      = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created At"))
    modified_at     = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_("Modified At"))
    is_staff        = models.BooleanField(_("staff"), default=False, help_text=_("Designates whether this user should be treated as staff. "),)
    is_active       = models.BooleanField(_("active"), default=False,
                            help_text=_(
                                "Designates whether this user should be treated as active. "
                                "Unselect this instead of deleting accounts."
                            ),
                        )

    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        db_table = "user"

    def __str__(self):
        return str(self.first_name)

    def fullname(self):
        return self.first_name + " " + self.last_name

class PasswordReset(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class UserPermissions(BaseModel):

    administer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_administer",
    )

    staff_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_permission_by_administer",
    )

    user_view = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether this user should be create,update,delete user. "
        ),
    )
    user_edit = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether this user should be create,update,delete user. "
        ),
    )
    user_delete = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether this user should be create,update,delete customer. "
        ),
    )

