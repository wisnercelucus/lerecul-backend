from django.urls import path

from frontend_views.api.views import (
                    FrontEndMenuLinkAPIView,
                    FrontEndMenuLinkListAPIView,
                    ObjectsFrontEndMenuLinkListAPIView,
                    )

urlpatterns = [
    # Your URLs...
    path('', FrontEndMenuLinkAPIView.as_view(), name='permissions'),
    path('list/', FrontEndMenuLinkListAPIView.as_view(), name='permissions'),    
    path('objects/', ObjectsFrontEndMenuLinkListAPIView.as_view(), name='permissions'),
    
]