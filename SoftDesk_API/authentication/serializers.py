from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',
                  'password',
                  'birthdate',
                  'can_data_be_shared',
                  'can_be_contacted')
