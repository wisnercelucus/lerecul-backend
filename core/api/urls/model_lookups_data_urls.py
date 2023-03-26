from django.urls import path

from core.api.views.model_lookups_data_views import (ModelLookupsDataAPIView, ModelIDAPIView,)

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', ModelLookupsDataAPIView.as_view()),
    path('id/', ModelIDAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)