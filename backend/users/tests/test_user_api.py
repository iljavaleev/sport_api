from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from users.models import Student, Coach

CREATE_USER_URL = reverse('users:create')
CREATE_STUDENT_URL = reverse('users:create_student')
CREATE_COACH_URL = reverse('users:create_coach')
CHANGE_PASSWORD_URL = reverse('users:change_password')
ME_URL = reverse('users:me')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserApiTests(TestCase):

    def setUp(self):
        self.super_client = APIClient()
        self.user_client = APIClient()
        self.super = get_user_model().objects.create_superuser(
            email='superemail@mail.ru',
            phone='+79227778899',
            password='suppass123',
        )
        self.super_client.force_authenticate(user=self.super)

        self.pre_student = create_user(
            email='student@example.com',
            phone='+79227778801',
            password='studentpass123',
        )
        self.pre_coach = create_user(
            email='coach@example.com',
            phone='+79227778802',
            password='coachpass123',
        )

    def test_create_user(self):
        """Создание юзера суперпользователем."""
        payload = {
            'email': 'test1@example.com',
            'password': 'testpass123',
            'phone': '+79226667798'
        }

        res = self.super_client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Проверка уникальности почтового адреса."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'phone': '+79226667799'
        }

        create_user(**payload)
        res = self.super_client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Проверка на слишком короткий адрес."""
        payload = {
            'email': 'test@example.com',
            'phone': '+79225667799',
            'password': 'pw',
        }

        res = self.super_client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_student_user(self):
        """Создание Студента."""
        payload = {
            'email': 'student@example.com',
            'username': 'username',
            'first_name': 'fname',
            'last_name': 'lname',
            'password': 'studentpass123',
            'phone': '+79227778801',
        }

        res = self.user_client.post(CREATE_STUDENT_URL, payload)

        student = Student.objects.get(user__email=payload['email'])
        self.assertEqual(student.user.is_student, True)
        self.assertEqual(student.username, payload['username'])

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_coach_user(self):
        """Создание Тренера."""

        payload = {
            'email': 'coach@example.com',
            'last_name': 'last_name',
            'username':'coach',
            'first_name': 'faname',
            'specialization':'ST',
            'password': 'coachpass123',
            'phone': '+79227778802',
        }

        res = self.user_client.post(CREATE_COACH_URL, payload)


        coach = Coach.objects.get(user__email=payload['email'])
        self.assertNotIn('password', res.data)
        self.assertEqual(coach.user.is_coach, True)
        self.assertEqual(coach.username, payload['username'])
        self.assertEqual(coach.specialization, payload['specialization'])

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_password(self):
        """Обновление токена."""
        payload = {
            'email': 'student@example.com',
            'username': 'username',
            'first_name': 'fname',
            'last_name': 'lname',
            'password': 'studentpass123',
            'phone': '+79227778801',
        }

        for_update_payload = {
            'old_password': payload['password'],
            'new_password': 'new_studentpass123'
        }

        resp = self.user_client.post(CREATE_STUDENT_URL, payload)
        self.assertIn('token', resp.data)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password
                        (for_update_payload['old_password']))

        token = get_object_or_404(Token, user=user)
        self.assertEqual(token.key, resp.data['token'])

        self.user_client.force_authenticate(user=user, token=token)

        res = self.user_client.patch(
            CHANGE_PASSWORD_URL,
            data=for_update_payload,
            headers={'Authorization': 'Token ' + resp.data['token']})

        self.assertTrue(user.check_password
                        (for_update_payload['new_password']))
        self.assertEqual(get_object_or_404(Token, user=user).key,
                         res.data['token'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_token_bad_credentials(self):
        """Проверка на неправильные данные."""
        create_user(email='test@example.com', phone='+79189991212',
                    password='goodpass')

        payload = {'email': 'test@example.com', 'phone':'+79189991212',
                   'password': 'badpass', 'username': 'username',
                   'first_name': 'fname', 'last_name': 'lname',}

        res = self.super_client.post(CREATE_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Проверка на неправильный email"""
        payload = {'email': 'student@example.com', 'password': 'badpass',
                   'username': 'username', 'first_name': 'fname',
                   'last_name': 'lname',}

        res = self.super_client.post(CREATE_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.user_client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_success(self):
        res = self.super_client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'phone': self.super.phone,
            'email': self.super.email,
        })

    def test_post_me_not_allowed(self):
        res = self.super_client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'email': 'updated@mail.ru',
                   'password': 'Updated_pass123'}

        res = self.super_client.patch(ME_URL, payload)

        self.super.refresh_from_db()
        self.assertEqual(self.super.email, payload['email'])
        self.assertTrue(self.super.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)