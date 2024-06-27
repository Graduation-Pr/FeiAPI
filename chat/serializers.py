from rest_framework import serializers
from .models import Message
from accounts.models import User
from asgiref.sync import sync_to_async


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "name")

    def get_name(self, obj):
        fname = obj.first_name.capitalize()
        lname = obj.last_name.capitalize()
        return f"{fname} {lname}"

class MessageSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'text', 'user', 'created', 'is_me']

    def get_is_me(self, obj):
        user = self.context['user']
        return obj.user == user