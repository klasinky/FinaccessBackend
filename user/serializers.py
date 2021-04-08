from datetime import datetime

from django.contrib.auth import password_validation, authenticate
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from core.models import Currency, User

class CurrencyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""
    currency = CurrencyModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'last_login',
            'is_active',
        )
        read_only_fields = (
            'last_login', 'is_active'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User SignUp Serializer"""
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_length=4,
        max_length=20,
    )

    name = serializers.CharField(min_length=2, max_length=35)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_length=4,
        max_length=255
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Verifica si las contraseñas coiciden"""
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")

        password_validation.validate_password(passwd)
        return data

    def create(self, validated_data):
        """Handle user and profile creation"""
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login"""

    email = serializers.EmailField(min_length=4, max_length=255)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Verifica los campos usuario y password"""
        user = authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError('Credenciales no válidas')
        user.last_login = datetime.now()
        user.save()
        self.context['user'] = user

        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar la contraseña"""
    old_password = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        extra_kwargs = {
            "new_password": {"write_only": True},
            "old_password": {"write_only": True},
        }
