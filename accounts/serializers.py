from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("No account with this phone number.")
        return value

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ["full_name", "phone_number", "password", "confirm_password"]
        # extra_kwargs = {
        #     "password": {"write_only": True},
        #     "full_name": {"required": True},
        #     "phone_number": {"required": True},
        # }

    def validate(self, attrs):
        errors = {}
        
        # if not attrs.get("full_name"):
        #     errors["full_name"] = ["This field is required."]
        if not attrs.get("phone_number"):
            errors["phone_number"] = ["This field is required."]
        if not attrs.get("password"):
            errors["password"] = ["This field is required."]
        if not attrs.get("confirm_password"):
            errors["confirm_password"] = ["This field is required."]

        if errors:
            raise serializers.ValidationError(errors)

        if attrs["password"] != attrs["confirm_password"]:
            errors["confirm_password"] = ["Passwords do not match"]

        try:
            validate_password(attrs["password"])
        except serializers.ValidationError as e:
            errors["password"] = list(e.messages)

        if not errors and User.objects.filter(phone_number=attrs["phone_number"]).exists():
            # Mask the message for security
            errors["phone_number"] = ["Invalid registration data."]

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            username=f"user_{validated_data['phone_number']}",
            # username=validated_data["phone_number"],
            phone_number=validated_data["phone_number"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
            is_verified=False
        )
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(phone_number=data["phone_number"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")

        # if not user.is_verified:
        #     raise serializers.ValidationError({
        #         "detail": "Account not verified. Please verify OTP to login."
        #     })
        
        data["user"] = user
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "phone_number": user.phone_number,
            },
        }


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        try:
            otp = OTP.objects.filter(
                phone_number=data["phone_number"], code=data["otp"], is_used=False
            ).latest("created_at")
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP")

        if not otp.is_valid():
            raise serializers.ValidationError("OTP expired or already used")

        otp.is_used = True
        otp.save()
        return data

    def save(self, **kwargs):
        user = User.objects.get(phone_number=self.validated_data["phone_number"])
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
