from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, DoctorProfile, PatientProfile
from pharmacy.models import Cart


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        # token["full_name"] = user.full_name

        return token


class RegisterPatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    role = serializers.CharField(read_only=True, default=User.Role.PATIENT)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "role",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        cart = Cart.objects.create(user=user)
        return user


class RegisterDoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    role = serializers.CharField(read_only=True, default=User.Role.DOCTOR)
    # full_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "role",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        # validated_data.pop("password")
        # validated_data.pop("role")
        # DoctorProfile.objects.create(user=user, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "city",
            "government",
            "image",
            "gender",
            "role",
        )


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = (
            "user",
            "bio",
            "verified",
            "rating",
        )


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = (
            "user",
            "birth_date",
        )
