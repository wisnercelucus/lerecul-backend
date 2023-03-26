from rest_framework import serializers

class FilteredDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    _id = serializers.UUIDField()
    name = serializers.CharField()


class FormLookupsSerializer(serializers.Serializer):
    _id = serializers.CharField()
    id = serializers.IntegerField()
    name = serializers.CharField()