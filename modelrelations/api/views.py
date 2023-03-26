from django.contrib.contenttypes.models import ContentType
from accounts.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core import serializers

from model_meta_data.api.views.model_meta_views import DeepLookupSerializer, LookupSerializer
from django.utils.translation import gettext_lazy as _

class RecordModelManyToManyDataAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        data = request.data
        #print(data)
        app_label = data.get("app_label")
        model_type = data.get("content_type")
        object_id = data.get("object_id")
        records = data.get("records")
        field = data.get("field")

        if model_type == 'userprofile':
            model_type = 'user'
            profile = UserProfile.objects.filter(pk=object_id)
            if profile.exists():
                user = profile.first().user
                object_id = user.id

        model_qs = ContentType.objects.filter(app_label=app_label, model=model_type)
        if model_qs.exists():
            Model = model_qs.first().model_class()
            fields = Model._meta.get_fields()
            targeted_field = [f for f in fields if f.name ==field]
            if len(targeted_field) != 1:
                return Response({"error": _("The field" + field + " does not exist on " + model_type)}, 
                status=status.HTTP_400_BAD_REQUEST)
            field =  targeted_field[0]
            if field.description != 'Many-to-many relationship':
                return Response({"error": _("The field " + field.name + " is not in many to many relationship on " + model_type)}, 
                status=status.HTTP_400_BAD_REQUEST) 
            obj_qs = Model.objects.filter(pk=object_id)
            if obj_qs.exists():
                record = obj_qs.first()
                m2m = getattr(record, field.name)
                existed_m2m = [r.pk for r in m2m.all()]
                for r in existed_m2m:
                    if r not in records:
                        to_remove_qs = m2m.filter(pk=r)
                        if to_remove_qs.exists():
                            m2m.remove(to_remove_qs.first())

                for v in records:
                    if v not in existed_m2m:
                        m2m.add(v)

                data_ = m2m.all()
                json_data = serializers.serialize('json', data_ )
        return Response(json_data , status=status.HTTP_200_OK)


class ModelManyToManyDataAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        data = request.data
        #print(data)

        app_label = data.get("app_label")
        model_type = data.get("content_type")
        field = data.get("field")
        object_id = data.get("object_id")

        if model_type == 'userprofile':
            model_type = 'user'
            profile = UserProfile.objects.filter(pk=object_id)
            if profile.exists():
                user = profile.first().user
                object_id = user.id

        model_qs = ContentType.objects.filter(app_label=app_label, model=model_type)
        if model_qs.exists():
            Model = model_qs.first().model_class()
            fields = Model._meta.get_fields()
            targeted_field = [f for f in fields if f.name ==field]
            #print(targeted_field)
            if len(targeted_field) != 1:
                return Response({"error": _("The field" + field + " does not exist on " + model_type)}, 
                status=status.HTTP_400_BAD_REQUEST)
            field =  targeted_field[0]
            if field.description != 'Many-to-many relationship':
                return Response({"error": _("The field " + field.name + " is not in many to many relationship on " + model_type)}, 
                status=status.HTTP_400_BAD_REQUEST) 
            obj_qs = Model.objects.filter(pk=object_id)

            if obj_qs.exists():
                record = obj_qs.first()
                m2m = getattr(record, field.name)
                data_ = m2m.all()
                json_data = serializers.serialize('json', data_ )

        return Response(json_data , status=status.HTTP_200_OK)


class GetRecordsForManyToManyRelation(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, object, format=None):
        data = request.data
        app_label = data.get("app_label")
        model_type = data.get("content_type")
        field = data.get("field")

        if model_type == 'userprofile':
            model_type = 'user'

        model_qs = ContentType.objects.filter(app_label=app_label, model=model_type)
        if model_qs.exists():
            Model = model_qs.first().model_class()
            fields = Model._meta.get_fields()
            targeted_field = [f for f in fields if f.name ==field]
            if len(targeted_field) != 1:
                return Response({"error": _("The field" + field + " does not exist on " + model_type)}, 
                status=status.HTTP_400_BAD_REQUEST)
            field =  targeted_field[0]
            if field.description != 'Many-to-many relationship':
                return Response({"error": _("The field " + field + " is not in many to many relationship on " + model_type)}, 
                status=status.HTTP_400_BAD_REQUEST) 
            related_model = field.related_model
            data = related_model.objects.all()
            if not related_model._meta.model_name in ['permission', 'group']:
                data = LookupSerializer(data, many=True).data
            else:
                data = DeepLookupSerializer(data, many=True).data
        return Response(data, status=status.HTTP_201_CREATED) 