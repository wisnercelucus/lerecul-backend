from django.http import Http404
#from accounts.api.permissions import PermissionDeniedError, check_user_permission
from core.api.pagination import StandardResultPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.gallery_serializers import (GalleryModelSerializer,
GalleryFormoLookupsSerializer, 
GalleryDetailsSerializer,
GalleryCreateSerializer, GalleryTableModelSerializer, HomeGalleryImagesModelSerializer, HomeGalleryModelSerializer,)
from core.models import Gallery as Model

from rest_framework import generics

class GalleryListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated,]
    serializer_class = GalleryTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return Model.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(GalleryListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class HommeGalleryAPIView(APIView):

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Banner.view_Banner')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        record_qs = Model.objects.filter(default=True)
        if record_qs.exists():
            record = record_qs.first()
            serialised_data = HomeGalleryModelSerializer(record, many=False).data
            return Response(serialised_data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)


class HommeGalleryImagesAPIView(APIView):

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Banner.view_Banner')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        record_qs = Model.objects.filter(default=True)
        if record_qs.exists():
            record = record_qs.first()
            serialised_data = HomeGalleryImagesModelSerializer(record, many=False).data
            return Response(serialised_data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)


class GalleryAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Gallery.view_Gallery')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        records = Model.objects.all()
        serialised_data = GalleryModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        #try:
        #    check_user_permission(request.user, 'Gallery.add_Gallery')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        default = data.get('default')

        if not default in ['', None]:
            if default:
                banners_defaults = Model.objects.filter(default=True)
                for d in banners_defaults:
                    d.default = False
                    d.save()

        serializer = GalleryCreateSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save(owner=request.user, updated_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GalleryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, uuid):
        try:
            return Model.objects.get(_id=uuid)
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Gallery.view_Gallery')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = GalleryDetailsSerializer(record)
        return Response(serializer.data)

    def put(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Gallery.change_Gallery')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        default = data.get('default')

        if not default in ['', None]:
            if default:
                banners_defaults = Model.objects.filter(default=True)
                for d in banners_defaults:
                    d.default = False
                    d.save()

        record = self.get_object(uuid)
        serializer = GalleryModelSerializer(record, data=data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Gallery.delete_Gallery')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormLookupsAPIView(APIView):
    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Gallery.view_Gallery')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        records = Model.objects.all()
        serialised_data = GalleryFormoLookupsSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)