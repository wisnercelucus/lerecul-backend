from loginactivity.api.serializers import LoginActivityModelSerializer, LoginActivityTableModelSerializer
from loginactivity.models import LoginActivity
from accounts.api.permissions import IsAdmin, PermissionDeniedError, check_user_permission
from core.api.pagination import StandardResultPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404



from rest_framework import generics

class LoginActivityListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LoginActivityTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return LoginActivity.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(LoginActivityListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class LoginActivityAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, _):
        try:
            check_user_permission(self.request.user, 'loginactivity.view_loginactivity')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        records = LoginActivity.objects.all()
        serialised_data = LoginActivityModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

class ManageLoginActivityAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, uuid):
        try:
            return LoginActivity.objects.get(_id=uuid)
        except LoginActivity.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'loginactivity.view_loginactivity')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = LoginActivityModelSerializer(record)
        return Response(serializer.data)

    def delete(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'loginactivity.delete_loginactivity')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

