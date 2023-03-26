from django.http import Http404
#from accounts.api.permissions import PermissionDeniedError, check_user_permission
from core.api.pagination import StandardResultPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.services_serializers import (HomeServiceModelSerializer, ServiceModelSerializer,
ServiceFormoLookupsSerializer, 
ServiceDetailsSerializer,
ServiceCreateSerializer, ServiceTableModelSerializer,)
from core.models import Service as Model

from rest_framework import generics

class HomeServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated, ]

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Service.view_Service')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        records = Model.objects.filter(in_slider=True)
        serialised_data = HomeServiceModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)


class ServiceListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated,]
    serializer_class = ServiceTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return Model.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(ServiceListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class ServiceAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Service.view_Service')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        records = Model.objects.all()
        serialised_data = ServiceModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        #try:
        #    check_user_permission(request.user, 'Service.add_Service')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = ServiceCreateSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save(owner=request.user, updated_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ServiceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, uuid):
        try:
            return Model.objects.get(_id=uuid)
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Service.view_Service')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = ServiceDetailsSerializer(record)
        return Response(serializer.data)

    def put(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Service.change_Service')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = ServiceModelSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'Service.delete_Service')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormLookupsAPIView(APIView):
    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'Service.view_Service')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        records = Model.objects.all()
        serialised_data = ServiceFormoLookupsSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)