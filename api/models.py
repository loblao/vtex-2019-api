# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=100)
    addr = models.CharField(max_length=250)
    api_token = models.CharField(max_length=64)


class AuthUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class APIUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    store = models.ForeignKey(Store, null=True, related_name='user_store')

    objects = AuthUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class SessionToken(models.Model):
    value = models.CharField(unique=True, max_length=32)
    expiration = models.DateTimeField()
    user = models.ForeignKey(APIUser, related_name='token_user')


STATUS_PEN = 0
STATUS_READY = 1
STATUS_PICKED_UP = 2

class OrderInfo(models.Model):
    user = models.ForeignKey(APIUser, related_name='order_user')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=32)
    store = models.ForeignKey(Store, related_name='order_store')
    price = models.FloatField()
    status = models.IntegerField(default=STATUS_PEN)
    expected_date = models.DateTimeField(null=True)
    payment_info = models.CharField(max_length=100)
    seller = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    desc = models.CharField(max_length=70)
