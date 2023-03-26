from core.api.serializers.lookup_serializer import get_lookups_data
from rest_framework import serializers
from core.models import Service as LOCAL_MODEL
from accounts.api.serializers.user_serialisers import UserNameSerializer, UserSlimSerializer


class HomeServiceModelSerializer(serializers.ModelSerializer):
    #images = serializers.SerializerMethodField()
    #is_owned = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        fields = ['name', 'featured_image', 'id', '_id', 'material_icon_code', 'description',]


class ServiceModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        fields = '__all__'

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOCAL_MODEL
        fields = '__all__'


class ServiceDetailsSerializer(serializers.ModelSerializer):
    owner = UserSlimSerializer(read_only=True)
    updated_by = UserSlimSerializer(read_only=True)
    content_type = serializers.SerializerMethodField()
    app_label = serializers.SerializerMethodField()
    is_owned = serializers.SerializerMethodField()
    lookups = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        exclude = ('deleted_at',)

    def get_content_type(self, obj):
        model_name = obj._meta.model_name
        return model_name

    def get_app_label(self, obj):
        app_label = obj._meta.app_label
        return app_label

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False


    def get_lookups(self, obj):
        return get_lookups_data(obj)


class ServiceSlimSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()
    object_model = serializers.SerializerMethodField()
    frontend_root = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        fields = ['uuid', 'name', 'object_model', 'id', '_id', 'frontend_root',]

    def get_uuid(self, obj):
        return obj._id

    def get_object_model(self, obj):
        return obj._meta.model_name

    def get_frontend_root(self, obj):
        return 'Services'

class ServiceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOCAL_MODEL
        fields = ['name',]

class ServiceFormoLookupsSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        fields = ['uuid', '_id', 'id', 'name',]

    def get_uuid(self, obj):
        return obj._id


class ServiceTableModelSerializer(serializers.ModelSerializer):
    owner = UserNameSerializer(read_only=True)
    updated_by = UserNameSerializer(read_only=True)
    is_owned = serializers.SerializerMethodField()

    
    class Meta:
        model = LOCAL_MODEL
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