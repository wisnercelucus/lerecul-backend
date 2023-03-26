from django.http import Http404
#from accounts.api.permissions import PermissionDeniedError, check_user_permission
from core.api.pagination import StandardResultPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.activities_serializers import (ActivityModelSerializer,
ActivityFormoLookupsSerializer, 
ActivityDetailsSerializer,
ActivityCreateSerializer, ActivityTableModelSerializer, HomeActivityModelSerializer,)
from core.models import Activity as Model

from rest_framework import generics

class ActivityListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated,]
    serializer_class = ActivityTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return Model.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(ActivityListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class HomeActivityAPIView(APIView):
    #permission_classes = [IsAuthenticated, ]

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Activity.view_Activity')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        records = Model.objects.filter(in_slider=True)
        serialised_data = HomeActivityModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)


class ActivityAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Activity.view_Activity')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        records = Model.objects.all()
        serialised_data = ActivityModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        #try:
        #    check_user_permission(request.user, 'Activity.add_Activity')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = ActivityCreateSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save(owner=request.user, updated_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ActivityDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, uuid):
        try:
            return Model.objects.get(_id=uuid)
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Activity.view_Activity')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = ActivityDetailsSerializer(record)
        return Response(serializer.data)

    def put(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Activity.change_Activity')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = ActivityModelSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Activity.delete_Activity')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormLookupsAPIView(APIView):
    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Activity.view_Activity')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        records = Model.objects.all()
        serialised_data = ActivityFormoLookupsSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)