from rest_framework import serializers
from frontend_views.models import FrontEndMenuLink

class FrontEndMenuLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontEndMenuLink
        fields = '__all__'



class FrontEndMenuLinkTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontEndMenuLink
        fields = '__all__'


class FrontEndMenuLinkNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontEndMenuLink
        fields = ['name',]