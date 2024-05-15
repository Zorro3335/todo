from rest_framework import serializers

from .models import ToDo
from django.contrib.auth.models import User


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    todo = ToDoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'todo']
