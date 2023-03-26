from django.urls import path
from ...api.views.room_service_views import (RoomServiceAPIView,
                                        RoomServiceDetailAPIView, 
                                        RoomServiceListAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', RoomServiceAPIView.as_view()),
    path('list/', RoomServiceListAPIView.as_view()),
    path('<str:uuid>/', RoomServiceDetailAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)