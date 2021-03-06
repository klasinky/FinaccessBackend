from datetime import datetime

from django.contrib.auth import password_validation, authenticate
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from app import settings
from core.models import Currency, User, Post, UserFollowing
from drf_extra_fields.fields import Base64ImageField


class CurrencyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer
        Se utiliza para crear / editar usuario
    """
    currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all()
    )
    profile_pic = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'username',
            'id',
            'name',
            'email',
            'last_login',
            'is_active',
            'currency',
            'profile_pic'
        )
        read_only_fields = (
            'last_login', 'is_active'
        )


class UserPrivateSerializer(serializers.ModelSerializer):
    """User private serializer"""
    currency = CurrencyModelSerializer(read_only=True)
    profile_pic = serializers.SerializerMethodField('get_profile_url')

    def get_profile_url(self, obj):
        request = self.context.get('request')
        url = None
        if obj.profile_pic:
            params = f'{settings.STATIC_URL}images{obj.profile_pic.url}'
            url = request.build_absolute_uri(params)
        return url

    class Meta:
        model = User
        fields = (
            'username',
            'id',
            'name',
            'email',
            'last_login',
            'is_active',
            'currency',
            'profile_pic'
        )
        read_only_fields = (
            'last_login', 'is_active'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User SignUp Serializer"""
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_length=4,
        max_length=12,
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
        """Verifica si las contrase??as coiciden"""
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contrase??as no coinciden")

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
            raise serializers.ValidationError('Credenciales no v??lidas')
        user.last_login = datetime.now()
        user.save()
        self.context['user'] = user

        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar la contrase??a"""
    old_password = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        new_password = data['new_password']
        password_validation.validate_password(new_password)
        return data

    class Meta:
        model = User
        extra_kwargs = {
            "new_password": {"write_only": True},
            "old_password": {"write_only": True},
        }


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    total_likes = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()
    total_posts = serializers.SerializerMethodField()
    is_your_profile = serializers.SerializerMethodField()
    is_follower = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField('get_profile_url')

    def get_profile_url(self, obj):
        request = self.context.get('request')
        url = None
        if obj.profile_pic:
            params = f'{settings.STATIC_URL}images{obj.profile_pic.url}'
            url = request.build_absolute_uri(params)
        return url

    def get_total_posts(self, obj) -> int:
        return Post.objects.filter(author=obj, is_active=True).count()

    def get_is_your_profile(self, obj) -> bool:
        request = self.context.get('request')
        return request.user == obj

    def get_is_following(self, obj) -> bool:
        """Indica si t?? sigues al usuario"""
        request = self.context.get('request')
        if request.user == obj:
            return False
        return UserFollowing.objects.filter\
            (user=request.user, following=obj).count() > 0

    def get_is_follower(self, obj):
        """Indica si el usuario te sigue"""
        request = self.context.get('request')
        if request.user == obj:
            return False
        return UserFollowing.objects.filter\
            (user=obj, following=request.user).count() > 0

    def get_total_likes(self, obj):
        total_likes: int = 0
        posts = Post.objects.filter(author=obj, is_active=True)
        for post in posts:
            total_likes += post.total_likes()
        return total_likes

    def get_total_followers(self, obj):
        return UserFollowing.objects.filter(following=obj).count()

    def get_total_following(self, obj):
        return UserFollowing.objects.filter(user=obj).count()

    class Meta:
        model = User
        fields = ('id', 'username','is_your_profile',
                  'total_likes', 'is_follower','profile_pic'
                  'total_followers', 'is_following'
                  'total_following', 'name','total_posts')
