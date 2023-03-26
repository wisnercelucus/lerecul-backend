from django.urls import path
from ...api.views.strengths_views import (HomeStrengthAPIView, StrengthAPIView,
                                        StrengthDetailAPIView, 
                                        StrengthListAPIView,)

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', StrengthAPIView.as_view()),
    path('list/', StrengthListAPIView.as_view()),
    path('list/home/', HomeStrengthAPIView.as_view()),
    path('<str:uuid>/', StrengthDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)