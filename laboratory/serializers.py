from rest_framework import serializers
from .models import Laboratory


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = ("name", "image", "rate", "city")


class LaboratoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = "__all__"
