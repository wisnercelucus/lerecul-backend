from django.urls import path
from .images_views import (FeaturedImageAPIView, FeaturedImageDetailAPIView, ObjectFeaturedImageListAPIView )
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', FeaturedImageAPIView.as_view()),
    path('<str:uuid>/', FeaturedImageDetailAPIView.as_view()),
     path('<str:app_label>/<str:object_name>/<str:uuid>/', ObjectFeaturedImageListAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)