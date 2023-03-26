from django.http import Http404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext as _

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from django.db.models import CharField, TextField
from django.db.models.functions import Lower

from core_forms.api.serializers import FilteredDataSerializer, FormLookupsSerializer

# from django.db import connection
# with connection.cursor() as cursor:
#    cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')

CharField.register_lookup(Lower)

TextField.register_lookup(Lower)
                                        


def get_or_404(Model, key=None):
    if not key:
        raise Http404
    record_qs = Model.objects.filter(pk=key)
    if record_qs.exists():
        return record_qs.first()
    else:
        raise Http404


class SearchFilteredDataAPIView(APIView):
    # permission_classes = [IsAuthenticated,]
    
    def post(self, request):
        app_label = request.data.get('app_label')
        object_name = request.data.get('model_type')
        keyword = request.data.get('keyword')


        data_res = []

        model_qs = ContentType.objects.filter(app_label=app_label, model=object_name)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(
                Q(name__icontains=keyword) |
                Q(_id__icontains=keyword))

            data_res = FilteredDataSerializer(obj_qs, many=True).data

            return Response(data_res, status=status.HTTP_200_OK)
        return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)


class FormLookupsAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        data = request.data
        app_label = data.get('app_label')
        content_type = data.get('content_type')
        model_qs = ContentType.objects.filter(
                            app_label=app_label, 
                            model=content_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            records = SomeModel.objects.all()
            data = FormLookupsSerializer(records, many=True).data
        return Response(data, status=status.HTTP_200_OK)
