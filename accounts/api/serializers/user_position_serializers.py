from accounts.api.serializers.user_serialisers import UserNameSerializer, UserSlimSerializer
from rest_framework import serializers
from accounts.models import UserPosition

class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition
        fields = '__all__'


class UserPositionDetailSerializer(serializers.ModelSerializer):
    owner = UserSlimSerializer(read_only=True)
    updated_by = UserSlimSerializer(read_only=True)
    content_type = serializers.SerializerMethodField()
    app_label = serializers.SerializerMethodField()

    class Meta:
        model = UserPosition
        fields = '__all__'

    def get_content_type(self, obj):
        model_name = obj._meta.model_name
        return model_name

    def get_app_label(self, obj):
        app_label = obj._meta.app_label
        return app_label


class PositionTableModelSerializer(serializers.ModelSerializer):
    owner = UserNameSerializer(read_only=True)
    updated_by = UserNameSerializer(read_only=True)
    is_owned = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPosition
        fields = ['created_at', 
                    'updated_at', 
                    'is_owned', 
                    'owner', 
                    'updated_by',
                    'name',
                    '_id', 
                    'id',]

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False


class UserPositionSlimForDetailSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()
    object_model = serializers.SerializerMethodField()
    frontend_root = serializers.SerializerMethodField()
    in_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPosition
        fields = ['uuid', 'name', 'object_model', '_id', 'id', 'frontend_root', 'in_admin',]

    def get_uuid(self, obj):
        return obj._id

    def get_object_model(self, obj):
        return obj._meta.model_name

    def get_frontend_root(self, obj):
        return 'positions'

    def get_in_admin(self, obj):
        return False