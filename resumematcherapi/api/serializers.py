from rest_framework import serializers
from core.models import *

class UserSerlializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    
class JobSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    rubric_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Job
        fields = ['id','name', 'jod_description', 'user_id', 'rubric_id', 'date_created', 'priority']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        rubric_id = validated_data.pop('rubric_id')
        user = User.objects.get(id=user_id)
        rubric = Rubric.objects.get(id=rubric_id)
        return Job.objects.create(user=user, rubric=rubric, **validated_data)

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields ='__all__'

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'