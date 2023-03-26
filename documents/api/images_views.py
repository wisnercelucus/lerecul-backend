from django.http import Http404
from documents.api.images_serializers import (FeaturedImageCreateSerializer, 
                                        FeaturedImageDetailsSerializer, 
                                        FeaturedImageModelSerializer, 
                                        featured_image_create_serializer,)
from accounts.api.permissions import PermissionDeniedError, check_user_permission, check_user_permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from documents.models import FeaturedImage
from rest_framework import generics
from django.utils.translation import gettext_lazy as _

from django.contrib.contenttypes.models import ContentType

def modify_input_for_multiple_docs(file, title):
    dict = {}
    dict['image'] = file
    dict['name'] = title
    return dict


class FeaturedImageCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        model_type = self.request.POST.get('content_type')
        pk = self.request.POST.get('object_id')

        return featured_image_create_serializer(
            model_type=model_type, pk=pk, FeaturedImage=None,
            user=self.request.user)


class FeaturedImageAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, _):
        #try:
        #    check_user_permission(self.request.user, 'FeaturedImages.view_FeaturedImage')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        FeaturedImages = FeaturedImage.objects.all()
        serialised_data = FeaturedImageDetailsSerializer(FeaturedImages, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        #try:
        #    check_user_permissions(self.request.user, ['FeaturedImages.add_FeaturedImage', 'FeaturedImages.add_recordFeaturedImagegroup'])
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        group_name = data.get("name")
        object_id = data.get("object_id")
        model_type = data.get("content_type")
        app_label = data.get("app_label")
        content_type = None

        model_qs = ContentType.objects.filter(app_label=app_label, model=model_type)
        
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(pk=object_id)
            content_type = model_qs.first()
            if obj_qs.exists():
                obj = obj_qs.first()
            else:
                return Response({"error": _("Object does not exist on object: " + model_type)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": _("Invalid content type")}, status=status.HTTP_400_BAD_REQUEST)

        files = dict((request.FILES).lists()).get('image')
        created_list = []
        failed_errors = []
        if files:
            for file in files:
                try:
                    FeaturedImage_modified = modify_input_for_multiple_docs(file, file.name)
                    FeaturedImage_modified['object_id'] = obj.id
                    FeaturedImage_modified['content_type'] = content_type.id
                    serailizer = FeaturedImageCreateSerializer(data=FeaturedImage_modified)
                    if serailizer.is_valid():
                        image = serailizer.save(owner=self.request.user, updated_by=self.request.user)
                        created_list.append(image)
                    else:
                        return Response({"error": serailizer.errors}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    failed_errors.append(str(e))
        
        if len(failed_errors) and len(created_list):
            return Response({"success": FeaturedImageCreateSerializer(created_list, many=True).data, "failed_errors": failed_errors}, status=status.HTTP_200_OK)
        elif len(created_list) and len(failed_errors) == 0:
            return Response({"success": FeaturedImageCreateSerializer(created_list, many=True).data}, status=status.HTTP_200_OK)
        elif len(failed_errors):
            return Response({"failed_errors": failed_errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": _("An unknown error occured.")}, status=status.HTTP_400_BAD_REQUEST)


class FeaturedImageDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, uuid):
        try:
            return FeaturedImage.objects.get(_id=uuid)
        except FeaturedImage.DoesNotExist:
            raise Http404

    def get(self, _, uuid):
        try:
            check_user_permission(self.request.user, 'FeaturedImages.view_FeaturedImage')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        FeaturedImage = self.get_object(uuid)
        serializer = FeaturedImageDetailsSerializer(FeaturedImage)
        return Response(serializer.data)

    def put(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'FeaturedImages.change_FeaturedImage')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        FeaturedImage = self.get_object(uuid)
        serializer = FeaturedImageModelSerializer(FeaturedImage, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, uuid):
        #try:
        #    check_user_permission(self.request.user, 'FeaturedImages.delete_FeaturedImage')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        FeaturedImage = self.get_object(uuid)
        FeaturedImage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ObjectFeaturedImageListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, app_label, object_name, uuid):
        #try:
        #    check_user_permissions(self.request.user, ['FeaturedImages.view_FeaturedImage', 'FeaturedImages.view_recordFeaturedImagegroup'])
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        model_qs = ContentType.objects.filter(app_label=app_label, model=object_name)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(_id=uuid)
            content_type = model_qs.first()
            if obj_qs.exists():
                obj = obj_qs.first()
                images = FeaturedImage.objects.filter(
                        content_type=content_type,
                        object_id=obj.id
                        )
        return Response(FeaturedImageModelSerializer(images, many=True).data, status=status.HTTP_200_OK)

