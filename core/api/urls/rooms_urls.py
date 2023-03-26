from django.urls import path
from ...api.views.rooms_views import (RoomAPIView,
                                        RoomDetailAPIView, 
                                        PublicRoomsFormFormsAPIView,
                                        PublicRoomDEtailsAPIView,
                                        RoomListAPIView, RoomsFormFormsAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', RoomAPIView.as_view()),
    path('public/', PublicRoomsFormFormsAPIView.as_view()),
    path('<str:uuid>/anonymous/', PublicRoomDEtailsAPIView.as_view()),
    path('list/', RoomListAPIView.as_view()),
    path('fill/', RoomsFormFormsAPIView.as_view()),
    path('<str:uuid>/', RoomDetailAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)