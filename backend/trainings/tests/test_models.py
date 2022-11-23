from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from users import models


class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""

        email = 'test@example.com'
        password = 'testpass123'
        phone = '+79226662211'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            phone='+79226662211',
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.phone, phone)
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
                                                        phone='+79226662211')
            self.assertEqual(user.email, expected)
            user.delete()

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='',
                                                 phone='+79226662211',
                                                 password='test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
            phone='+79226662211')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
