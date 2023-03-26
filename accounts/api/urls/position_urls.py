from django.urls import path

from accounts.api.views import (
                    PositionAPIView,
                    ManagePositionAPIView,
                    PositionListAPIView,
                    )

urlpatterns = [
    # Your URLs...
    path('', PositionAPIView.as_view(), name='users'),
    path('list/', PositionListAPIView.as_view(), name='users'),
    path('<str:uuid>/', ManagePositionAPIView.as_view(), name='position_manager'),
    
]