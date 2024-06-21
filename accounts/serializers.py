from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from doctor.models import DoctorBooking
from .models import User, DoctorProfile, PatientProfile
from pharmacy.models import Cart
from django.contrib.auth import authenticate


import base64
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str) and data.startswith("data:image"):
            # base64 encoded image - decode it
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
        elif isinstance(data, str):
            # base64 encoded string but without data:image prefix
            imgstr = data
            data = ContentFile(base64.b64decode(imgstr), name="temp.png")
        return super().to_internal_value(data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get("password")

        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("This username is not registered.")

        # Authenticate the user
        if user and authenticate(username=username, password=password):
            data = super().validate(attrs)
            cart_id = user.user_cart.id
            data["username"] = user.username
            data["email"] = user.email
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name
            data["role"] = user.role
            data["cart_id"] = cart_id

            return data
        else:
            raise serializers.ValidationError("Incorrect password.")

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["role"] = user.role

        return token


from rest_framework import serializers
from .models import User


class RegisterPatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    role = serializers.CharField(read_only=True, default=User.Role.PATIENT)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
            "password",
            "confirm_password",
            "role",
            "city",
            "government",
            "gender",
            "phone_number",
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email address is already registered."
            )
        return value

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
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
            "password",
            "confirm_password",
            "role",
            "city",
            "government",
            "gender",
            "phone_number",
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email address is already registered."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        cart = Cart.objects.create(user=user)

        return user


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("name",)

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "username",
            "phone_number",
            "city",
            "government",
            "gender",
            "role",
            "birth_date",
            "image_url",  # Add image_url to the fields
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class UpdateUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(
        required=False
    )  # Allow phone number to be optional
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "password",
            "email",
            "first_name",
            "last_name",
            "image",
            "phone_number",  # Include phone_number field in the serializer
            "role",
            "birth_date",
            "city",
            "government",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Format birth_date as day-month-year
        if instance.birth_date:
            formatted_date = instance.birth_date.strftime("%d-%m-%Y")
        else:
            formatted_date = None
        data["birth_date"] = formatted_date
        return data

    def validate_phone_number(self, value):
        if value and len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = (
            "user",
            "bio",
            "verified",
            "rating",
            "experience",
            "doctor_patients",
            "specialization",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ("user",)
