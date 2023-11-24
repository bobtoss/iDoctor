from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import User, Services
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "login", "password", "email", "name", "surname", "company"]

    def create(self, validated_data):
        user = User.objects.create(login=validated_data['login'], password=validated_data['password'],
                                   email=validated_data['email'], name=validated_data['name'],
                                   surname=validated_data['surname'], company=validated_data['company'],
                                   )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

    def create(self, validated_data):
        service = Services.objects.create(name=validated_data['name'], image=validated_data['image'],
                                   url=validated_data['url'])

        service.save()

        return service

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#
#     def validate(self, attrs):
#         print(attrs)
#         self.user = User.objects.get(phone_number=phone_number)
#         # Do the verification with the phone_code here, if error, return a response with an error status code
#
#         refresh = self.get_token(self.user)
#
#         data['refresh'] = text_type(refresh)
#         data['access'] = text_type(refresh.access_token)
#
#         return data
