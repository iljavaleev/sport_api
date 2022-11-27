import uuid
import os
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import EmailMessage


def send_email(email, password):
    email = EmailMessage(
        'Credentials to access sport_api',
        f'username: {email}, password: {password}',
        'sport_api@gmail.com',
        [f'{email}']
    )
    email.send()


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        if not phone:
            raise ValueError('User must have a phone number.')
        send_email(email, password)
        user = self.model(
            email=self.normalize_email(email),
            phone=PhoneNumber.from_string(phone_number=phone,
                                          region='RU').as_e164,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(email=email,
                                phone=phone,
                                password=password)

        user.is_staff = True
        user.is_superuser = True
        user.is_student = False
        user.is_coach = False
        user.save(using=self._db)

        return user

class StudentManager(BaseUserManager):
    def create_user(self, user, first_name, last_name, username,
                    **extra_fields):

        user.is_student = True
        user.save(using=self._db)
        student = self.model(
            user=user,
            first_name=first_name,
            last_name=last_name,
            username=username,
            **extra_fields
        )
        student.save(using=self._db)

        return student

class CoachManager(BaseUserManager):
    def create_user(self,user, specialization, first_name,
                    last_name, username, **extra_fields):

        user.is_coach = True
        user.save(using=self._db)
        coach = self.model(
            user=user,
            specialization=specialization,
            first_name=first_name,
            last_name=last_name,
            username=username,
            **extra_fields
        )
        coach.save(using=self._db)

        return coach

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone = PhoneNumberField(null=False, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

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
    sports_titles = models.TextField(
        blank=True,
        max_length=500,
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
    objects = StudentManager()
    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Coach(models.Model):
    class Specialization(models.TextChoices):
        STRENGTH = 'ST', 'Strength'
        POWER = 'PO', 'Power'
        SPEED = 'SP', 'Speed'
        TECHNICAL = 'TE', 'Technical'

    user = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 primary_key=True)

    students = models.ManyToManyField(
        Student,
        related_name='coaches',
        blank=True
    )

    specialization = models.CharField(
        max_length=2,
        choices=Specialization.choices,
        blank=False,
    )

    experience = models.IntegerField(default=0)

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
    achievements = models.TextField(
        blank=True,
        max_length=500,
    )
    objects = CoachManager()
    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
