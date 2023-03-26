from django.urls import path
from ...api.views.activities_views import (ActivityAPIView,
                                        ActivityDetailAPIView, 
                                        ActivityListAPIView, HomeActivityAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', ActivityAPIView.as_view()),
    path('list/', ActivityListAPIView.as_view()),
    path('list/home/', HomeActivityAPIView.as_view()),
    path('<str:uuid>/', ActivityDetailAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)