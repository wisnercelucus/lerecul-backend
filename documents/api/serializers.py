from accounts.api.serializers.user_serialisers import (UserSlimSerializer,)
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from documents.models import Document, FeaturedImage, RecordDocumentGroup
from accounts.models import User


class DocumentModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = '__all__'

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class DocumentDetailsSerializer(serializers.ModelSerializer):
    owner = UserSlimSerializer(read_only=True)
    updated_by = UserSlimSerializer(read_only=True)
    url = serializers.SerializerMethodField()
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = Document
        exclude = ('deleted_at', 'id',)

    def get_url(self, obj):
        url = obj.document.url
        return url

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class DocumentGroupSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = RecordDocumentGroup
        exclude = ('deleted_at', 'id',)

    def get_documents(self, obj):
        docs = obj.document_set.all()
        return DocumentDetailsSerializer(docs, many=True).data

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False


def document_create_serializer(model_type=None, pk=None, document=None, user=None):
    class DocumentCreateSerializer(serializers.ModelSerializer):
        owner = UserSlimSerializer(read_only=True)

        class Meta:
            model = Document
            fields = [
                'id',
                'content',
                'created_at',
                'object_id',
                'owner',
                'document',
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.pk = pk
            return super(DocumentCreateSerializer, self).__init__(*args, **kwargs)

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
            document = Document.objects.create_by_model_type(
                model_type, pk, document, main_user)
            if document:
                return document
            return Document()
    return DocumentCreateSerializer


class DocumentTableModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = Document
        exclude = ('deleted_at',)

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class DocumentGroupTableModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()
    
    class Meta:
        model = RecordDocumentGroup
        exclude = ('deleted_at',)

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False


class RecordDocumentGroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordDocumentGroup
        fields = ['name',]


class DocumentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name',]


class FeaturedImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedImage
        fields = '__all__'