from rest_framework import serializers
from core.models import *

class UserSerlializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'