from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from home.api.views import BookNowAPIView, ContactMessageCreateAPIView, NewsSubscriberCreateAPIView

urlpatterns = [
    path('book/', BookNowAPIView.as_view()),
    path('create/', NewsSubscriberCreateAPIView.as_view(), name='create-subscriber'),
    path('send/', ContactMessageCreateAPIView.as_view(), name='send-message'),
]

urlpatterns = format_suffix_patterns(urlpatterns)