from rest_framework import serializers
from . models import VirtualWalletUser


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = VirtualWalletUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'first_name', 'last_name', 'password', 'email', 'birth_date')

    def create(self, validated_data):
        user = VirtualWalletUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



