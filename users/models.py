from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number=None, email=None, password=None, **extra_fields):
        if not mobile_number and not email:
            raise ValueError("Either mobile_number or email must be set")

        # Fallback for username (required field on AbstractUser internally)
        if mobile_number:
            extra_fields.setdefault('username', str(mobile_number))
        else:
            extra_fields.setdefault('username', email)

        user = self.model(mobile_number=mobile_number, email=email, **extra_fields)

        # Set password only if provided
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        return user

    def create_superuser(self, mobile_number=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError("Superusers must have a password.")

        return self.create_user(mobile_number=mobile_number, email=email, password=password, **extra_fields)

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    mobile_number = PhoneNumberField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ])
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    def __str__(self):
        # Return a string representation, such as the username, email, or stringified mobile number
        return self.username or str(self.mobile_number) or "User"