from loginactivity.models import LoginActivity
from accounts.api.serializers.user_serialisers import UserSlimSerializer
from rest_framework import serializers

class LoginActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginActivity
        fields = '__all__'


class LoginActivityTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginActivity
        fields = '__all__'


class LoginActivityDetailSerializer(serializers.ModelSerializer):
    user = UserSlimSerializer(read_only=True)
    content_type = serializers.SerializerMethodField()
    app_label = serializers.SerializerMethodField()

    class Meta:
        model = LoginActivity
        exclude = ('deleted_at',)

    def get_content_type(self, obj):
        model_name = obj._meta.model_name
        return model_name

    def get_app_label(self, obj):
        app_label = obj._meta.app_label
        return app_label