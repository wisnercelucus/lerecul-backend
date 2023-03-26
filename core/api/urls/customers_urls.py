from django.urls import path
from ...api.views.customers_views import (CustomerAPIView,
                                        CustomerDetailAPIView, 
                                        CustomerListAPIView,)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', CustomerAPIView.as_view()),
    path('list/', CustomerListAPIView.as_view()),
    path('<str:uuid>/', CustomerDetailAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)