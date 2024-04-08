import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.contrib import admin

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, default=None,blank=True, null=True)
    last_name = models.CharField(max_length=30, default=None,blank=True, null=True)
    email = models.EmailField(max_length=500, default=None,blank=True, null=True)
    password = models.CharField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "first_name",
        "last_name",
        "email",
        "created_at",
        "updated_at"
    )

admin.site.register(User, UserAdmin)