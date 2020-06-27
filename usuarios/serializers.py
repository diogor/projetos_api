from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'avatar',
                  'last_name', 'apresentacao', 'projetos')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'avatar',
                  'last_name', 'apresentacao', 'password')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'avatar', 'last_name',
                  'apresentacao')
