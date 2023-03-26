from django.urls import path

from .views import (
    LoginActivityAPIView,
    LoginActivityListAPIView,
    ManageLoginActivityAPIView
                    )

urlpatterns = [
    # Your URLs...
    path('', LoginActivityAPIView.as_view(), name='user_profile'),
    path('list/', LoginActivityListAPIView.as_view(), name='user_profile'),
    path('<str:uuid>/', ManageLoginActivityAPIView.as_view(), name='user_profile'),
    
]