from django.http import Http404
from documents.api.serializers import (DocumentCreateSerializer, 
                                        DocumentDetailsSerializer, DocumentGroupSerializer, 
                                        DocumentModelSerializer, 
                                        document_create_serializer,)
from accounts.api.permissions import PermissionDeniedError, check_user_permission, check_user_permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from documents.models import Document, RecordDocumentGroup
from rest_framework import generics

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


def modify_input_for_multiple_docs(file, title, group):
    dict = {}
    dict['document'] = file
    dict['name'] = title
    dict['group'] = group
    return dict


class DocumentCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        model_type = self.request.POST.get('content_type')
        pk = self.request.POST.get('object_id')

        return document_create_serializer(
            model_type=model_type, pk=pk, document=None,
            user=self.request.user)


class DocumentAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, _):
        try:
            check_user_permission(self.request.user, 'documents.view_document')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        documents = Document.objects.all()
        serialised_data = DocumentDetailsSerializer(documents, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            check_user_permissions(self.request.user, ['documents.add_document', 'documents.add_recorddocumentgroup'])
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

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
                object = obj_qs.first()
            else:
                return Response({"error": _("Object does not exist on object: " + model_type)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": _("Invalid content type")}, status=status.HTTP_400_BAD_REQUEST)

        group = RecordDocumentGroup()
        group.name = group_name
        group.content_type = content_type
        group.object_id = object.id
        group.owner = request.user
        group.updated_by = request.user
        group.save()

        files = dict((request.FILES).lists()).get('document')
        created_list = []
        failed_errors = []
        if files:
            for file in files:
                try:
                    document_modified = modify_input_for_multiple_docs(file, file.name, group.id)
                    serailizer = DocumentCreateSerializer(data=document_modified)
                
                    if serailizer.is_valid():
                        serailizer.save(owner=self.request.user, updated_by=self.request.user)
                        created_list.append(serailizer.data)
                    else:
                        return Response({"error": serailizer.errors}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    failed_errors.append(str(e))
        
        if len(failed_errors) and len(created_list):
            return Response({"group": DocumentGroupSerializer(group, many=False).data, "success": created_list, "failed_errors": failed_errors}, status=status.HTTP_200_OK)
        elif len(created_list) and len(failed_errors) == 0:
            return Response({"group": DocumentGroupSerializer(group, many=False).data, "success": created_list}, status=status.HTTP_200_OK)
        elif len(failed_errors):
            return Response({"failed_errors": failed_errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": _("An unknown error occured.")}, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, uuid):
        try:
            return Document.objects.get(_id=uuid)
        except Document.DoesNotExist:
            raise Http404

    def get(self, _, uuid):
        try:
            check_user_permission(self.request.user, 'documents.view_document')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        document = self.get_object(uuid)
        serializer = DocumentDetailsSerializer(document)
        return Response(serializer.data)

    def put(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'documents.change_document')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        document = self.get_object(uuid)
        serializer = DocumentModelSerializer(document, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, uuid):
        try:
            check_user_permission(self.request.user, 'documents.delete_document')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        document = self.get_object(uuid)
        group = document.group
        document.delete()

        if group.document_set.all().count():
            return Response({"empty_group": False}, status=status.HTTP_200_OK)
        else:
            group.delete()
            return Response({"empty_group": True}, status=status.HTTP_200_OK)



class ObjectDocumentListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, app_label, object_name, uuid):
        try:
            check_user_permissions(self.request.user, ['documents.view_document', 'documents.view_recorddocumentgroup'])
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        groups = []
        model_qs = ContentType.objects.filter(app_label=app_label, model=object_name)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(_id=uuid)
            # content_type = model_qs.first()
            if obj_qs.exists():
                object = obj_qs.first()
                groups = RecordDocumentGroup.objects.filter_by_instance(object)

            groups = DocumentGroupSerializer(groups, many=True).data
                
        
        return Response(groups, status=status.HTTP_200_OK)

