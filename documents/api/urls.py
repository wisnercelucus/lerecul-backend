from django.urls import path
from .views import (DocumentAPIView, DocumentDetailAPIView, ObjectDocumentListAPIView )
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', DocumentAPIView.as_view()),
    path('<str:uuid>/', DocumentDetailAPIView.as_view()),
     path('<str:app_label>/<str:object_name>/<str:uuid>/', ObjectDocumentListAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)