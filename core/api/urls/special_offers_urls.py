from django.urls import path

from ...api.views.special_offers_views import (SpecialOfferAPIView,
                                         SpecialOfferDetailAPIView, SpecialOfferListAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', SpecialOfferAPIView.as_view()),
    path('list/', SpecialOfferListAPIView.as_view()),
    path('<str:uuid>/', SpecialOfferDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)