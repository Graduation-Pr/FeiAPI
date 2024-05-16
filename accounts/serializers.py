from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from doctor.models import DoctorBooking
from .models import User, DoctorProfile, PatientProfile
from pharmacy.models import Cart
from django.contrib.auth import authenticate


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
            "city",
            "government",
            "gender",
            "phone_number"
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
            "city",
            "government",
            "gender",
            "phone_number"
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
            "birth_date"
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(
        required=False
    )  # Allow phone number to be optional

    class Meta:
        model = User
        fields = [
            "password",
            "email",
            "first_name",
            "last_name",
            "phone_number",  # Include phone_number field in the serializer
            "role",
            "birth_date",
            "gender",
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


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # doctor_patients = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = (
            "user",
            "bio",
            "verified",
            "rating",
            "experience",
            "doctor_patients"
        )

    # def get_doctor_patients(self):
    #     doctor_patients = self.context["doctor_patients"]
    #     return doctor_patients





class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = (
            "user",
            # "birth_date",
        )
