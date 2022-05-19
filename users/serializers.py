import email
from django.contrib.auth.models import User
from rest_framework import serializers, validators


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"write_only": True},
            "username": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "Username already exists."
                    )
                ],
            },
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already exists."
                    )
                ],
            },
        }


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        extra_kwargs = {
            "username" : {"required": False},
            "email" : {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def update(self, instance, validated_data):
        if(validated_data.get('first_name')):
            instance.first_name = validated_data.get('first_name')
        else: return 0
        if(validated_data.get('last_name')):
            instance.last_name = validated_data.get('last_name')
        else: return 0

        if(validated_data.get('email')):
            if User.objects.exclude(username=instance.username).filter(email=validated_data.get('email')).exists():
                return 1
            instance.email = validated_data.get('email')
        #instance.username = validated_data['username']

        instance.save()

        return instance
