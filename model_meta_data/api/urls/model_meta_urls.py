from django.urls import path
from ...api.views.model_meta_views import (ModelMetaFieldsAPIView,
ModelMetaManyToManyFieldsAPIView,
 ModelMetaFieldsForDetailAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('<str:objectname>/fields/', ModelMetaFieldsAPIView.as_view()),
    path('<str:objectname>/fields/details/', ModelMetaFieldsForDetailAPIView.as_view()),
    path('<str:objectname>/fields/many-to-many/', ModelMetaManyToManyFieldsAPIView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)