from django.urls import path

from accounts.api.views import (
                    PermissionListAPIView,
                    ObjectsPermissionListAPIView,
                    ObjectPermissionListAPIView,
                    PermissionListAPIView,
                    PermissionTabListAPIView,
                    )

urlpatterns = [
    # Your URLs...
    path('', PermissionListAPIView.as_view(), name='permissions'),
    path('list/', PermissionTabListAPIView.as_view(), name='permissions'),
    path('objects/', ObjectsPermissionListAPIView.as_view(), name='permissions'),
    path('object/<str:app_label>/<str:content_type>/', ObjectPermissionListAPIView.as_view(), name='permissions'),  
    
]