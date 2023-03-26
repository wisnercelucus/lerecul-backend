from accounts.api.serializers.user_serialisers import (UserSlimSerializer,)
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from documents.models import FeaturedImage
from accounts.models import User


class FeaturedImageModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedImage
        fields = '__all__'

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class FeaturedImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedImage
        fields = '__all__'


class FeaturedImageDetailsSerializer(serializers.ModelSerializer):
    owner = UserSlimSerializer(read_only=True)
    updated_by = UserSlimSerializer(read_only=True)
    url = serializers.SerializerMethodField()
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedImage
        exclude = ('deleted_at', 'id',)

    def get_url(self, obj):
        url = obj.FeaturedImage.url
        return url

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class FeaturedImageGroupSerializer(serializers.ModelSerializer):
    FeaturedImages = serializers.SerializerMethodField()
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedImage
        exclude = ('deleted_at', 'id',)

    def get_FeaturedImages(self, obj):
        docs = obj.FeaturedImage_set.all()
        return FeaturedImageDetailsSerializer(docs, many=True).data

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False


def featured_image_create_serializer(model_type=None, pk=None, FeaturedImage=None, user=None):
    class FeaturedImageCreateSerializer(serializers.ModelSerializer):
        owner = UserSlimSerializer(read_only=True)

        class Meta:
            model = FeaturedImage
            fields = [
                'id',
                'content',
                'created_at',
                'object_id',
                'owner',
                'FeaturedImage',
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.pk = pk
            return super(FeaturedImageCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, _):
            model_type = self.initial_data['content_type']
            pk = self.initial_data['object_id']
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists():
                raise serializers.ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(pk=pk)
            if not obj_qs.exists():
                raise serializers.ValidationError("This is not a valid Model")
            return self.initial_data

        def create(self, validated_data):
            model_type = validated_data.get('content_type')
            pk = validated_data.get('object_id')
            main_user = None
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            FeaturedImage = FeaturedImage.objects.create_by_model_type(
                model_type, pk, FeaturedImage, main_user)
            if FeaturedImage:
                return FeaturedImage
            return FeaturedImage()
    return FeaturedImageCreateSerializer


class FeaturedImageTableModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedImage
        exclude = ('deleted_at',)

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class FeaturedImageGroupTableModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()
    
    class Meta:
        model = FeaturedImage
        exclude = ('deleted_at',)

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False


class RecordFeaturedImageGroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedImage
        fields = ['name',]


class FeaturedImageNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedImage
        fields = ['name',]


class FeaturedImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedImage
        fields = '__all__'