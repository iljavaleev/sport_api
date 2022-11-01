from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from users import models


class ModelTests(TestCase):
    """Test models."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fields = {
            'username':'test',
            'first_name':'first_name',
            'last_name':'last_name',
            'role':'ST'
        }

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""

        email = 'test@example.com'
        password = 'testpass123'


        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            **ModelTests.fields,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, ModelTests.fields['username'])
        self.assertEqual(user.first_name, ModelTests.fields['first_name'])
        self.assertEqual(user.last_name, ModelTests.fields['last_name'])
        self.assertEqual(user.role, ModelTests.fields['role'])
        self.assertTrue(user.check_password(password))

        user.delete()

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email,
                                                        password='sample123',
                                                        **ModelTests.fields)
            self.assertEqual(user.email, expected)
            user.delete()

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='',
                                                 password='test123',
                                                 **ModelTests.fields)

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
            **ModelTests.fields
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
