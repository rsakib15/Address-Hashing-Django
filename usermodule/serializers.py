from rest_framework import serializers
from usermodule.models import User
import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('address', 'hash')
    