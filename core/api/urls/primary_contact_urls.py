from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core.api.views.primary_contact_views import PrimaryContactAPIView

urlpatterns = [
    path('', PrimaryContactAPIView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)