import uuid

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

from user.models import User

class Beer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, default=None,blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Hops(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, default=None,blank=True, null=True)

    beer = models.ForeignKey(Beer, on_delete=models.SET_NULL, null=True, related_name='hops')

    def __str__(self):
        return self.name

class Malts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, default=None,blank=True, null=True)

    beer = models.ForeignKey(Beer, on_delete=models.SET_NULL, null=True, related_name='malts')

    def __str__(self):
        return self.name

class BeerAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "name",
        "created_at",
        "updated_at"
    )

admin.site.register(Beer, BeerAdmin)