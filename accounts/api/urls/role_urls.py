from django.urls import path

from accounts.api.views import (
                    RoleAPIView,
                    ManageRoleAPIView,
                    RoleListAPIView,
                    )

urlpatterns = [
    # Your URLs...
    path('', RoleAPIView.as_view(), name='users'),
    path('list/', RoleListAPIView.as_view(), name='users'),
    path('<str:uuid>/', ManageRoleAPIView.as_view(), name='role_manager'),
    
]