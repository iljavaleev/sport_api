import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManger(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, role,
                    password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(username=username, email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name,
                          role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, last_name,
                         password, role='AD', **extra_fields):

        user = self.create_user(username=username,
                                password=password,
                                email=self.normalize_email(email),
                                first_name=first_name,
                                last_name=last_name, role=role, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        STUDENT = 'ST', 'Student'
        COACH = 'CO', 'Coach'
        ADMIN = 'AD', 'Admin'

    is_active = models.BooleanField(default=True,)
    is_staff = models.BooleanField(default=False,)
    sports_titles = models.TextField(
        blank=True,
        max_length=500,
    )

    first_name = models.CharField(
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=False
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )

    role = models.CharField(
        max_length=20,
        blank=False,
        choices=Role.choices,
    )

    email = models.EmailField(
        blank=False,
        max_length=254,
        unique=True,
    )

    weight = models.DecimalField(
        blank=True,
        max_digits=5,
        decimal_places=2,
        null=True,
    )

    height = models.DecimalField(
        blank=True,
        max_digits=5,
        decimal_places=2,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManger()
    # # importing datetime module
    # import datetime
    #
    # # creating an instance of
    # # datetime.date
    # d = datetime.date(1997, 10, 19)

    @property
    def is_coach(self):
        return self.role == self.Role.COACH

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
