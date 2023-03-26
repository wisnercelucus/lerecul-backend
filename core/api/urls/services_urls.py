from django.urls import path
from ...api.views.services_views import (HomeServiceAPIView, ServiceAPIView,
                                        ServiceDetailAPIView, 
                                        ServiceListAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', ServiceAPIView.as_view()),
    path('list/', ServiceListAPIView.as_view()),
    path('list/home/', HomeServiceAPIView.as_view()),
    path('<str:uuid>/', ServiceDetailAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)