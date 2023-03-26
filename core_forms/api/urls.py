from django.urls import path
from core_forms.api.views import (
                    SearchFilteredDataAPIView,
                    FormLookupsAPIView,
                    )
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
   
    path('form-lookups/', FormLookupsAPIView.as_view(), name='form_lookups'),
    path('search-filtered-data/', SearchFilteredDataAPIView.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)