from rest_framework import serializers
from accounts.models import UserProfile


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'