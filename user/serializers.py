from rest_framework import serializers
from . models import VirtualWalletUser


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = VirtualWalletUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'birth_date')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = VirtualWalletUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


