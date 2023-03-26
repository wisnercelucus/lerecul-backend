from django.urls import path
from ...api.views.gallery_views import (GalleryAPIView,
                                        GalleryDetailAPIView,
                                        HommeGalleryAPIView, 
                                        GalleryListAPIView, HommeGalleryImagesAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', GalleryAPIView.as_view()),
    path('list/', GalleryListAPIView.as_view()),
    path('list/home/', HommeGalleryAPIView.as_view()),
    path('list/home/images/', HommeGalleryImagesAPIView.as_view()),
    path('<str:uuid>/', GalleryDetailAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)