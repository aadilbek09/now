from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Mijoz ro'yxatdan o'tishi uchun serializer."""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password2': "Parollar mos emas."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            password=validated_data['password'],
            role=User.Role.USER,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Joriy foydalanuvchi ma'lumotlarini qaytarish uchun (/api/auth/me)."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'role', 'date_joined', 'avatar')
        read_only_fields = fields


class UserUpdateSerializer(serializers.ModelSerializer):
    """Profil tahrirlash uchun serializer — faqat ruxsat etilgan maydonlar."""

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'avatar')


class EaturkishTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Oddiy login uchun token serializer — javobga foydalanuvchi
    ma'lumotlarini ham qo'shib beradi.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class AdminTokenObtainPairSerializer(EaturkishTokenObtainPairSerializer):
    """
    Admin login uchun token serializer — faqat role=admin bo'lgan
    foydalanuvchilarga token beradi.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != User.Role.ADMIN:
            raise serializers.ValidationError(
                "Faqat admin huquqiga ega foydalanuvchilar kira oladi."
            )
        return data
