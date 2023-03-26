import uuid
import os
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from core.utils.models import TimeStamp, UUIDInjector
from core.utils.exceptions import ExtensionNotAcceptableError

User = settings.AUTH_USER_MODEL

def ressource_doc_path(_, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    allowed_ext = [
        'pdf', 'doc', 'docx',
        'txt', 'odt', 'xlsx',
        'xls', 'ppt', 'pptx',
        'csv', 'json', 'zip',
        'rar', 'png', 'jpg',
        'ts', 'md', 'html',
        'go', 'r', 'rb',
        'c', 'htm', 'calc',
        'py',
        'jpeg', 'gif', ]

    if not ext.lower() in allowed_ext:
        raise ExtensionNotAcceptableError(ext)

    return os.path.join('uploads/meal/ressources/', filename)


def featured_image_path(_, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    allowed_ext = [
        'png', 'jpg',
        'jpeg', 'gif', ]

    if not ext.lower() in allowed_ext:
        raise ExtensionNotAcceptableError(ext)

    return os.path.join('uploads/meal/ressources/', filename)


class DocumentGroupManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(DocumentGroupManager, self).filter(
            content_type=content_type,
            object_id=obj_id)
        return qs

    def create_by_model_type(self, model_type, pk, document, user):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(pk=pk)
            if obj_qs.exists():
                instance = self.model()
                instance.document = document
                instance.owner = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                instance.updated_by = user
                instance.save()
                return instance
            return ("Could not create it")
        return None


class RecordDocumentGroup(TimeStamp, UUIDInjector):
    name = models.CharField(max_length=250)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    updated_by = models.ForeignKey(User,
                                   related_name="group_document_modifier",
                                   on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name

    objects = DocumentGroupManager()

    class Meta:
        permissions = (
                    ("approve_recorddocumentgroup", "Can approve document group"),
                    )

        # verbose_name_plural = "indicator categories"


class Document(TimeStamp, UUIDInjector):
    group = models.ForeignKey(RecordDocumentGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    document = models.FileField(max_length=500,
                                null=True, blank=True,
                                upload_to=ressource_doc_path)
    updated_by = models.ForeignKey(User,
                                   related_name="document_modifier",
                                   on_delete=models.CASCADE, null=True)

    @property
    def object_model(self):
        return self.content_type.model

    def __str__(self) -> str:
        return self.name


    class Meta:
        permissions = (
                    ("approve_document", "Can approve document"),
                    )

        # verbose_name_plural = "indicator categories"

class FeaturedImage(TimeStamp, UUIDInjector):

    name = models.CharField(max_length=250)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    image = models.ImageField(max_length=500,
                                null=True, blank=True,
                                upload_to=featured_image_path)
    updated_by = models.ForeignKey(User,
                                   related_name="featured_image_modifier",
                                   on_delete=models.CASCADE, null=True)

    @property
    def object_model(self):
        return self.content_type.model

    def __str__(self) -> str:
        return self.name


    class Meta:
        permissions = (
                    ("approve_featured_image", "Can approve featured image"),
                    )

        # verbose_name_plural = "indicator categories"