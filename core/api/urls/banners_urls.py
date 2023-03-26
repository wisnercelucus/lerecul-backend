from django.urls import path
from ...api.views.banners_views import (BannerAPIView,
                                        BannerDetailAPIView, 
                                        BannerListAPIView, HommeBannerAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', BannerAPIView.as_view()),
    path('list/', BannerListAPIView.as_view()),
    path('list/home/', HommeBannerAPIView.as_view()),
    path('<str:uuid>/', BannerDetailAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)