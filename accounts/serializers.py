from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from . models import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('PATIENT', 'Patient'),
    ]

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'phone',
            'password',
            'confirm_password'
        ]

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists")

        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError("Phone number already exists")

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        if not attrs['phone'].isdigit() or len(attrs['phone']) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits")

        password_validation.validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()

    class Meta:
        model = PatientProfile
        fields = [
            "id",
            "user",
            "patient_image",
            "age",
            "hospital_name",
            "phone",
            "address",
            "blood_group",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        # Create user using RegisterSerializer (real password)
        user = RegisterSerializer().create(user_data)

        profile = PatientProfile.objects.create(
            user=user,
            **validated_data
        )
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        # Update user
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Update profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Old password is incorrect")

        password_validation.validate_password(attrs['new_password'], user)
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    
