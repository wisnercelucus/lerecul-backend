from django.http import Http404
#from accounts.api.permissions import PermissionDeniedError, check_user_permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import UserProfile as Model


class PrimaryContactAPIView(APIView):

    def get_object(self):
        try:
            return Model.objects.get(primary_contact_for_customer_care=True)
        except Model.DoesNotExist:
            raise Http404

    def get(self, _):
        record = self.get_object()
        serializer = {'name': record.user.name, 
                    'phone_home': record.phone_home,
                    'phone_mobile': record.phone_mobile,
                    'phone_work': record.phone_work,
                    'email': record.user.email
                    }
        return Response(serializer, status=status.HTTP_200_OK)


