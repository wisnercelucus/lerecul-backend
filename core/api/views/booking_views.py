from django.http import Http404
#from accounts.api.permissions import PermissionDeniedError, check_user_permission
from core.api.pagination import StandardResultPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils.util_funcs import str_to_date

from ..serializers.booking_serializers import (BookingModelSerializer,
                                                BookingCreateSerializer,
                                                BookingDetailsSerializer, 
                                                BookingTableModelSerializer,)
from ...models import Booking
from rest_framework import generics


class BookingListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = BookingTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return Booking.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(BookingListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        #try:
        #    check_user_permission(request.user, 'core.view_Booking')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN) 

        records = Booking.objects.all()
        serialised_data = BookingModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        #try:
        #    check_user_permission(request.user, 'core.add_Booking')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['start_on'] = str_to_date(data.get('start_on'))
        data['end_on'] = str_to_date(data.get('end_on'))
        serializer = BookingCreateSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save(owner=request.user, updated_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get_object(self, uuid):
        try:
            return Booking.objects.get(_id=uuid)
        except Booking.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'core.view_Booking')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        context = {"request": request}
        serializer = BookingDetailsSerializer(record, context=context)
        return Response(serializer.data)

    def put(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'core.change_Booking')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data=request.data
        record = self.get_object(uuid)
        data['start_on'] = str_to_date(data.get('start_on'))
        data['end_on'] = str_to_date(data.get('end_on'))
        serializer = BookingCreateSerializer(record, data=data)
        try:
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        #try:
        #    check_user_permission(request.user, 'core.delete_Booking')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)