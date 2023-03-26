from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class LookupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    _id = serializers.UUIDField()
    name = serializers.CharField()


class DeepLookupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

def _check_required(field) -> bool:
    return not field.blank or not field.null


def is_skipable(field) -> bool:
    skipable_fields = ['object_id',
                       'content_type',
                       'deleted_at',
                       'content_object',
                       'created_at',
                       'updated_at',
                       'user',
                       'owner',
                       'updated_by',
                       'geography',
                       'status',
                       'rejected_at',
                       'rejected_by',
                       'reviewed_at',
                       'reviewed_by',
                       'approved_at',
                       'approved_by',
                       'completed_at',
                       'completed_by',
                       'assigned_by',
                       'deffered_at',
                       'deffered_by',
                       'submitted_by',
                       'submitted_at',
                       'recalled_by',
                       'recalled_at',
                       'approver_notified',
                       'user_notified_on_decision',
                       'turn_inprogress_by',
                       'turn_inprogress_at',
                       'pk',
                       'groups',
                       'user_permissions',
                       'permissions',
                       'id',
                       'date_joined',
                       'is_superuser',
                       '_id',
                       'password',
                       'last_login',
                       'new_account_notified',
                       'published_at',
                       'published_by',
                       ]
    return field.name in skipable_fields


def is_skipable_many_to_many(field) -> bool:
    skipable_fields = ['object_id',
                       'content_type',
                       'deleted_at',
                       'content_object',
                       'created_at',
                       'updated_at',
                       'user',
                       'owner',
                       'updated_by',
                       'status',
                       'rejected_at',
                       'reviewed_at',
                       'approved_at',
                       'completed_at',
                       'pk',
                       'id',
                       'date_joined',
                       'is_superuser',
                       'groups',
                       '_id',
                       'password',
                       'last_login',
                       ]
    return field.name in skipable_fields


class ModelMetaFieldsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, _, objectname, *args, **kwargs):
        if objectname == 'role':
            objectname = 'userrole'
            
        if objectname == 'activitie':
            objectname = 'activity'

        if objectname == 'position':
            objectname = 'userposition'

        if objectname == 'account':
            objectname = 'userprofile'
            
        model_fields = []

        model_qs = ContentType.objects.filter(model=objectname)

        if model_qs.exists():
            Model = model_qs.first().model_class()
            
            fields = Model._meta.get_fields()

            for field in fields:
                # for field in SomeModel._meta.fields:

                if is_skipable(field):
                    continue
                if 'description' in dir(field):
                    new_field = {'name': field.name, 'is_required': _check_required(field)}

                    if 'Foreign Key' in field.description:
                        new_field['description'] = 'Lookup field'
                        # print(dir(field))
                        # print(field.flatchoices)

                    elif 'String' in field.description:
                        new_field['description'] = 'Short text'
                        new_field['max_length'] = field.max_length

                        if field.choices:
                            new_field['choices'] = []
                            for c in field.choices:
                                new_field['choices'].append(c[0])
                    elif 'integer' in field.description:
                        new_field['description'] = 'Integer'
                    elif 'Floating' in field.description:
                        new_field['description'] = 'Float'
                    elif 'without time' in field.description:
                        new_field['description'] = 'Date'
                    elif 'with time' in field.description:
                        new_field['description'] = 'DateTime'
                    elif 'Boolean' in field.description:
                        new_field['description'] = 'Boolean'
                    else:
                        new_field['description'] = field.description

                    if field.related_model:
                        new_field['related_model'] = field.related_model._meta.model_name
                        new_field['app_label'] = field.related_model._meta.app_label
                        # new_field['lookups'] = LookupSerializer(field.related_model.objects.all(), many=True).data

                    model_fields.append(new_field)

            return Response({'fields': model_fields}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {"Object " + objectname + ' does not exist.'}},
                            status=status.HTTP_400_BAD_REQUEST)


class ModelMetaFieldsForDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, _, objectname, *args, **kwargs):
        model_fields = []
        model_qs = ContentType.objects.filter(model=objectname)
        if model_qs.exists():
            Model = model_qs.first().model_class()
            fields = Model._meta.get_fields()
            for field in fields:
                if is_skipable(field):
                    continue
                if 'description' in dir(field):
                    new_field = {'name': field.name, 'is_required': _check_required(field)}
                    if field.description == 'Many-to-many relationship':
                        continue
                    if 'Foreign Key' in field.description:
                        new_field['description'] = 'Lookup field'
                        # print(dir(field))
                        # print(field.flatchoices)
                    elif 'String' in field.description:
                        new_field['description'] = 'Short text'
                        new_field['max_length'] = field.max_length

                        if field.choices:
                            new_field['choices'] = []
                            for c in field.choices:
                                new_field['choices'].append(c[0])
                    elif 'integer' in field.description:
                        new_field['description'] = 'Integer'
                    elif 'Floating' in field.description:
                        new_field['description'] = 'Float'
                    elif 'without time' in field.description:
                        new_field['description'] = 'Date'
                    elif 'with time' in field.description:
                        new_field['description'] = 'DateTime'
                    elif 'Boolean' in field.description:
                        new_field['description'] = 'Boolean'
                    else:
                        new_field['description'] = field.description
                    if field.related_model:
                        new_field['related_model'] = field.related_model._meta.model_name
                        new_field['app_label'] = field.related_model._meta.app_label
                    model_fields.append(new_field)
            return Response({'fields': model_fields}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {_("Object " + objectname + ' does not exist.')}},
                            status=status.HTTP_400_BAD_REQUEST)


class ModelMetaManyToManyFieldsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, _, objectname, *args, **kwargs):
        if objectname == 'account':
            objectname = 'user'

        model_fields = []
        model_qs = ContentType.objects.filter(model=objectname)
        if model_qs.exists():
            Model = model_qs.first().model_class()
            fields = Model._meta.get_fields()

            for field in fields:
                if is_skipable_many_to_many(field):
                    continue
                if 'description' in dir(field):
                    name = field.name
                    if name == 'forms':
                        continue
                    new_field = {'name': name, 'is_required': _check_required(field)}
                    if field.description != 'Many-to-many relationship':
                        continue
                    new_field['description'] = field.description
                    if field.related_model:
                        new_field['related_model'] = field.related_model._meta.model_name
                        new_field['app_label'] = field.related_model._meta.app_label
                    model_fields.append(new_field)
            return Response({'fields': model_fields}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {_("Object " + objectname + ' does not exist.')}},
                            status=status.HTTP_400_BAD_REQUEST)

