from rest_framework import serializers
from .models import Message
from accounts.models import User

class MessageSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "is_me", "text", "created"]

    def get_is_me(self, obj):
        return self.context["user"] == obj.user


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "name")

    def get_name(self, obj):
        fname = obj.first_name.capitalize()
        lname = obj.last_name.capitalize()

        return fname + " " + lname
