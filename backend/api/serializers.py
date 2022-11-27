from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import Student, Coach
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password



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


class WorkerSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()


    class Meta:
        fields = ['username', 'first_name', 'last_name', 'email', 'password',
                  'phone']

    def get_email(self, obj):
        return obj.user.email

    def get_password(self, obj):
        return obj.user.password

    def get_phone(self, obj):
        return obj.user.phone

    def pop_data_and_create_object(self, data, model):
        user = self.initial_data.get('user')
        try:
            return model.objects.create_user(user=user,
                                             **data)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError({
                'errors': 'This user is not exists. Contact the head coach'
            })


    def create(self, validated_data):
        return self.pop_data_and_create_object(validated_data, self.Meta.model)


class StudentSerializer(WorkerSerializer):
    class Meta:
        model = Student
        fields = WorkerSerializer.Meta.fields + ['sports_titles','weight',
                                                 'height', 'date_of_birth']

class CoachSerializer(WorkerSerializer):

    class Meta:
        model = Coach
        fields = WorkerSerializer.Meta.fields + ['specialization',
                                                 'experience', 'achievements']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value