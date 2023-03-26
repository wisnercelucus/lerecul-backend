from frontend_views.api.seralizers import FrontEndMenuLinkSerializer
from rest_framework import serializers
from accounts.models import User, UserPosition, UserProfile


class UserPositionSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = UserPosition
        fields = ['uuid', 'name', 'id', '_id',]

    def get_uuid(self, obj):
        if obj:
            return obj._id
        return None

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserTableModelSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()
    object_model = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['uuid', 'name', 'object_model', '_id', 'id', 'username', 'profile', 'is_active',]

    def get_uuid(self, obj):
        return obj._id

    def get_object_model(self, obj):
        return obj._meta.model_name

    def get_profile(self, obj):
        profile = obj.user_profile
        return UserProfileDetailSerializer(profile).data


class UserSlimSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()
    frontend_root = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'uuid', 'id', '_id', 'name', 'username', 'frontend_root',]

    def get_uuid(self, obj):
        return obj._id

    def get_frontend_root(self, obj):
        return 'accounts'

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name',]

class UserSlimForDetailSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()
    object_model = serializers.SerializerMethodField()
    frontend_root = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['uuid', 'name', 'object_model', '_id', 'id', 'username', 'frontend_root',]

    def get_uuid(self, obj):
        return obj._id

    def get_object_model(self, obj):
        return obj._meta.model_name

    def get_frontend_root(self, obj):
        return 'accounts'


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSlimSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['_id', 'id', 'last_name', 'first_name', 'user',]


class AccountForDetailSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()
    object_model = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['uuid', 'name', 'object_model', '_id', 'id', 'username', 'profile', 'is_active',]

    def get_uuid(self, obj):
        return obj._id

    def get_object_model(self, obj):
        return obj._meta.model_name

    def get_profile(self, obj):
        profile = obj.user_profile
        return UserProfileDetailSerializer(profile).data


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


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

class FullUserProfileModelSerializer(serializers.ModelSerializer):
    user = UserSlimSerializer(read_only=True)
    approver = UserSlimSerializer(read_only=True)
    owner = UserSlimSerializer(read_only=True)
    updated_by = UserSlimSerializer(read_only=True)
    avatar = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    app_label = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    frontend_views = serializers.SerializerMethodField()
    position = UserPositionSlimForDetailSerializer(read_only=True)
    

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return 'https://www.kindpng.com/picc/m/421-4212275_transparent-default-avatar-png-avatar-img-png-download.png'


    def get_content_type(self, obj):
        model_name = obj._meta.model_name
        return model_name

    def get_app_label(self, obj):
        app_label = obj._meta.app_label
        return app_label

    def get_permissions(self, obj):
        user = obj.user
        permissions = user.user_permissions.all()
        permission_ids = [p.id for p in permissions]
        return permission_ids

    def get_frontend_views(self, obj):
        user = obj.user
        views = user.frontend_views.all()
        views_ids = [p.id for p in views]
        return views_ids

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


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSlimForDetailSerializer(read_only=True)
    avatar = serializers.SerializerMethodField()
    frontend_views = serializers.SerializerMethodField()
    position = UserPositionSlimForDetailSerializer(read_only=True)
    user_permissions_codes = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['_id', 'id', 
                    'last_name', 
                    'first_name', 
                    'user', 
                    'avatar', 
                    'frontend_views', 
                    'position',
                    'user_permissions_codes',
                     ]

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return 'https://www.kindpng.com/picc/m/421-4212275_transparent-default-avatar-png-avatar-img-png-download.png'

    def get_user_permissions_codes(self, obj):
        permissions_codes = obj.user.get_user_permission_codes()
        return permissions_codes

    def get_frontend_views(self, obj):
        views = obj.user.get_user_all_frontend_views()
        data = FrontEndMenuLinkSerializer(views, many=True).data
        return data

class UserFormoLookupsSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['uuid', '_id', 'id', 'name', 'username',]

    def get_uuid(self, obj):
        return obj._id