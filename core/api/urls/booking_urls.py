from django.urls import path

from ...api.views.booking_views import (BookingAPIView,
                                         BookingDetailAPIView, BookingListAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', BookingAPIView.as_view()),
    path('list/', BookingListAPIView.as_view()),
    path('<str:uuid>/', BookingDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)