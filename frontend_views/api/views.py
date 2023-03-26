
from accounts.api.permissions import IsAdmin
from frontend_views.api.seralizers import FrontEndMenuLinkSerializer, FrontEndMenuLinkTableModelSerializer
from core.api.pagination import StandardResultPagination
from rest_framework import (status, permissions, generics,)
from frontend_views.models import FrontEndMenuLink
from rest_framework.response import Response
# from rest_framework.views import APIView
from accounts.models import UserProfile
from django.contrib.contenttypes.models import ContentType


from rest_framework import generics

class FrontEndMenuLinkListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = FrontEndMenuLinkTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return FrontEndMenuLink.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(FrontEndMenuLinkListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class FrontEndMenuLinkAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = FrontEndMenuLinkSerializer

    queryset = FrontEndMenuLink.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(FrontEndMenuLinkAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class ObjectsFrontEndMenuLinkListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = FrontEndMenuLinkSerializer

    def get(self, request):
        links = FrontEndMenuLink.objects.all()
        return Response(self.serializer_class(links, many=True).data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        model_type = data.pop('content_type')
        object_id = data.pop('object_id')
        app_label = data.pop('app_label')

        if model_type == 'userprofile':
            model_type = 'user'
            profile = UserProfile.objects.filter(pk=object_id)
            if profile.exists():
                object_id = profile.first().user.id

        model_qs = ContentType.objects.filter(app_label=app_label, model=model_type)

        if model_qs.exists():
            Model = model_qs.first().model_class()
            record_qs = Model.objects.filter(pk=object_id)

            if record_qs.exists():
                record = record_qs.first()

                incomin_frontend_views = []
                record_frontend_views = record.frontend_views.all()

                existed_frontend_views_ids = [p.id for p in record_frontend_views]
                data_keys = data.keys()

                for key in data_keys:
                    if data.get(key) in [None, '']:
                        continue
                    for p_id in data.get(key):
                        if not p_id in incomin_frontend_views:
                            incomin_frontend_views.append(int(p_id))

                for p_id in incomin_frontend_views:
                    if p_id not in existed_frontend_views_ids:
                        perm = FrontEndMenuLink.objects.filter(pk=p_id)
                        record.frontend_views.add(perm.first())

                for p in record_frontend_views:
                    if not p.id in incomin_frontend_views:
                        record.frontend_views.remove(p) 

                return_data = self.serializer_class(record.frontend_views.all(), many=True)
                return Response(return_data.data, status=status.HTTP_200_OK)
            return Response({"error": "We could not identify the record with id " + object_id}, status=status.HTTP_200_OK)
        return Response({"error": "No such object " + model_type}, status=status.HTTP_200_OK)

