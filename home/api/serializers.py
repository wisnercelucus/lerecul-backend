from rest_framework import serializers
from home.models import (NewsSubscriber,
						 ContactMessage
						 )


class NewsSubscriberModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = NewsSubscriber
		fields = ['email']


class ContactMessageModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContactMessage
		fields = '__all__'


class ContactMessageTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'


class NewsSubscriberTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSubscriber
        fields = '__all__'
