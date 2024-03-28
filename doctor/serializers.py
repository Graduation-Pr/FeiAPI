from rest_framework import serializers
from accounts.models import (
    DoctorProfile,
)  # Adjust the import path according to your project structure


class DoctorListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    government = serializers.CharField(source="user.government")
    city = serializers.CharField(source="user.city")

    # Assuming 'rating' is directly on the DoctorProfile model as per your previous setup

    class Meta:
        model = DoctorProfile
        fields = ("first_name", "last_name", "government", "rating", "city")
