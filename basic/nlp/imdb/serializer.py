from rest_framework import serializers
from basic.nlp.korean_classify.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'