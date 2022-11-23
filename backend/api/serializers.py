from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import Student, Coach
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        phone = get_object_or_404(get_user_model(), email=email).phone
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
            phone=phone
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


def pop_email_and_create_object(obj, data, model):
    email = obj.initial_data.get('my_email')
    try:
        return model.objects.create_user(email=email, **data)
    except get_user_model().DoesNotExist:
        raise serializers.ValidationError({
            'errors': 'This email is not exists. Contact the head coach'
        })

class StudentSerializer(serializers.ModelSerializer):
    my_email = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [ 'username', 'first_name', 'last_name', 'sports_titles',
                   'weight', 'height', 'date_of_birth', 'my_email']

    def get_my_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        return pop_email_and_create_object(self,validated_data, self.Meta.model)


class CoachSerializer(serializers.ModelSerializer):
    my_email = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = ['my_email', 'username', 'first_name', 'last_name',
                  'specialization', 'experience', 'achievements']

    def get_my_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        return pop_email_and_create_object(self, validated_data,
                                           self.Meta.model)
