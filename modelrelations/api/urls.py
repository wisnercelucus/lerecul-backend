from django.urls import path
from .views import (RecordModelManyToManyDataAPIView, 
ModelManyToManyDataAPIView,
GetRecordsForManyToManyRelation,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('many-to-many-data-record/', RecordModelManyToManyDataAPIView.as_view()),
    path('many-to-many-data/', ModelManyToManyDataAPIView.as_view()),
    path('<str:object>/records/', GetRecordsForManyToManyRelation.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)