from django.urls import path
from ...api.views.kitchens_views import (HommeKitchenAPIView, KitchenAPIView,
                                        KitchenDetailAPIView, 
                                        KitchenListAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', KitchenAPIView.as_view()),
    path('list/', KitchenListAPIView.as_view()),
    path('list/home/', HommeKitchenAPIView.as_view()),
    path('<str:uuid>/', KitchenDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)