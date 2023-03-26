from django.urls import path

from ...api.views.coupons_views import (CouponAPIView,
                                         CouponDetailAPIView, CouponListAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', CouponAPIView.as_view()),
    path('list/', CouponListAPIView.as_view()),
    path('<str:uuid>/', CouponDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)