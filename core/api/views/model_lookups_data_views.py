from django.contrib.contenttypes.models import ContentType
from core.api.pagination import StandardResultPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework import generics
from django.utils.translation import gettext_lazy as _

class LookupDataTableSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    _id = serializers.UUIDField()
    name = serializers.CharField()

def get_normal_model(objectname: str) -> str:
        if objectname == 'sector':
            objectname = 'developmentsector'

        if objectname == 'role':
            objectname = 'userrole'

        if objectname == 'position':
            objectname = 'userposition'

        if objectname == 'categorie' or objectname == 'categories':
            objectname = 'indicatorcategory'

        if objectname == 'countrie':
            objectname = 'country'

        if objectname == 'communitie':
            objectname = 'community'

        if objectname == 'approvalrequest':
            objectname = 'approval'

        return objectname


class ModelLookupsDataAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LookupDataTableSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self, *args, **kwargs):
        data = self.request.GET
        master_model = data.get('model')
        master_model_uuid = data.get('model_uuid')
        lookup_model = data.get('target_model')
        
        master_model = get_normal_model(master_model)
        lookup_model = get_normal_model(lookup_model)

        model_qs = ContentType.objects.filter(model=master_model)
        print(model_qs)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            record_qs = SomeModel.objects.filter(_id=master_model_uuid)
            if record_qs.exists():
                record = record_qs.first()
                attr = lookup_model + '_set'
                try:
                    qs = getattr(record, attr).all().order_by('pk')
                    return qs
                except Exception as e:
                    print(e)
                    return []
            return []
        return []


class ModelIDAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        data = request.data
        model = data.get('model')
        uuid = data.get('uuid')

        model_qs = ContentType.objects.filter(model=model)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            record_qs = SomeModel.objects.filter(_id=uuid)
            if record_qs.exists():
                return Response({"id": record_qs.first().id}, status=status.HTTP_200_OK)
            else:
                return Response({"error": _("Record with _id " + uuid + ' does not exist.')}, status=status.HTTP_200_OK)

        else:
            return Response({"error": _("Model with name " + model + ' does not exist.')}, status=status.HTTP_200_OK)