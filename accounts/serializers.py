# django imports
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate
# rest imports
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# python imports
import base64
# internal imports
from .models import User, DoctorProfile, PatientProfile
from pharmacy.models import Cart

class Base64ImageField(serializers.ImageField):
    """
    Custom serializer field to handle Base64 encoded images.
    """
    def to_internal_value(self, data):
        if isinstance(data, str):
            # Check if data is a Base64 string with a prefix
            if data.startswith("data:image"):
                format, imgstr = data.split(";base64,")
                ext = format.split("/")[-1]
            else:
                imgstr = data
                ext = "png"
            # Decode Base64 string to an image file
            data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
        return super().to_internal_value(data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer to include additional user data in the token.
    """
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get("password")

        # Check if the username exists
        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError("This username is not registered.")
        # Authenticate the user
        if not authenticate(username=username, password=password):
            raise serializers.ValidationError("Incorrect password.")

        # Get the standard token data
        data = super().validate(attrs)
        # Add custom user data to the response
        user_info = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "cart_id": user.user_cart.id
        }
        data.update(user_info)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        user_info = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
        return token

class RegisterSerializer(serializers.ModelSerializer):
    """
    Base serializer for user registration.
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    image = Base64ImageField(required=False, allow_null=True)

    def validate_email(self, value):
        # Ensure email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value

    def validate(self, attrs):
        # Ensure passwords match
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create_user(self, validated_data, role):
        # Remove confirm_password from validated data
        validated_data.pop("confirm_password")
        # Create the user and associated cart
        user = User.objects.create_user(**validated_data)
        Cart.objects.create(user=user)
        # Assign role to the user
        user.role = role
        user.save()
        return user

class RegisterPatientSerializer(RegisterSerializer):
    """
    Serializer for patient registration.
    """
    role = serializers.CharField(read_only=True, default=User.Role.PATIENT)

    class Meta:
        model = User
        fields = [
            "username", "email", "first_name", "last_name", "image",
            "password", "confirm_password", "role", "city", "government",
            "gender", "phone_number"
        ]

    def create(self, validated_data):
        return self.create_user(validated_data, User.Role.PATIENT)

class RegisterDoctorSerializer(RegisterSerializer):
    """
    Serializer for doctor registration.
    """
    role = serializers.CharField(read_only=True, default=User.Role.DOCTOR)

    class Meta:
        model = User
        fields = [
            "username", "email", "first_name", "last_name", "image",
            "password", "confirm_password", "role", "city", "government",
            "gender", "phone_number"
        ]

    def create(self, validated_data):
        return self.create_user(validated_data, User.Role.DOCTOR)

class SimpleUserSerializer(serializers.ModelSerializer):
    """
    Simple serializer for basic user information.
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("name",)

    def get_name(self, obj):
        # Concatenate first and last name
        return f"{obj.first_name} {obj.last_name}"


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed user information.
    """
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "full_name", "email", "username", "phone_number", "city",
            "government", "gender", "role", "birth_date", "image_url"
        ]
        
    def get_image_url(self, obj):
        request = self.context.get("request")
        if request and obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    """
    role = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(required=False)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "password", "email", "first_name", "last_name", "image",
            "phone_number", "role", "birth_date", "city", "government"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Format birth_date as day-month-year
        data["birth_date"] = instance.birth_date.strftime("%d-%m-%Y") if instance.birth_date else None
        return data

    def validate_phone_number(self, value):
        # Ensure phone number is exactly 10 digits
        if value and len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

class DoctorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for doctor profile information.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "user", "bio", "verified", "rating", "experience",
            "doctor_patients", "specialization"
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

class PatientProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for patient profile information.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ("user",)