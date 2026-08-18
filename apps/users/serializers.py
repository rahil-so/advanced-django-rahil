from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not '@' in value:
            raise serializers.ValidationError('Email address is not valid')
        return value

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User is not active')
        data['user'] = user
        return data




class UserBriefSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id', 'username','email', 'full_name', 'avatar',
        ]
        read_only_fields = [
            'id', 'email'
        ]

    def get_full_name(self, object):
        return f'{object.first_name} {object.last_name}'

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not '@' in value:
            raise serializers.ValidationError('Email address is not valid')
        return value

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            if email in password:
                raise serializers.ValidationError('Email address is not valid')
        else:
            raise serializers.ValidationError('Email address is not valid')
        user = authenticate(email=email, password=password)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['username','']




