from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupDetailSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    app_label = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'

    def get_content_type(self, obj):
        model_name = obj._meta.model_name
        return model_name

    def get_app_label(self, obj):
        app_label = obj._meta.app_label
        return app_label

