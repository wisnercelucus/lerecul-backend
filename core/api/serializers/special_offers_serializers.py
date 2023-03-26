from core.api.serializers.lookup_serializer import get_lookups_data
from rest_framework import serializers

from core.utils.exceptions import IncorrectDateRangeError
from core.models import SpecialOffer as LOCAL_MODEL
from core.utils.util_funcs import correct_timeline
from accounts.api.serializers.user_serialisers import UserNameSerializer, UserSlimSerializer


class SpecialOfferModelSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        fields = '__all__'

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class SpecialOfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOCAL_MODEL
        fields = '__all__'


    def validate(self, data):
        start_on = self.initial_data.get('start_on')
        end_on = self.initial_data.get('end_on')
        if not correct_timeline(start_on, end_on):
            raise IncorrectDateRangeError("End date must be in future compared to start date")
        return data



class SpecialOfferSlimSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()
    object_model = serializers.SerializerMethodField()
    frontend_root = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        fields = ['uuid', 'name', 'object_model', 'id', '_id',  'frontend_root',]

    def get_uuid(self, obj):
        return obj._id

    def get_object_model(self, obj):
        return obj._meta.model_name

    def get_frontend_root(self, obj):
        return 'SpecialOffers'



class SpecialOfferDetailsSerializer(serializers.ModelSerializer):
    owner = UserSlimSerializer(read_only=True)
    updated_by = UserSlimSerializer(read_only=True)
    content_type = serializers.SerializerMethodField()
    app_label = serializers.SerializerMethodField()
    is_owned = serializers.SerializerMethodField()
    #related_to_add = serializers.SerializerMethodField()
    lookups = serializers.SerializerMethodField()

    class Meta:
        model = LOCAL_MODEL
        exclude = ('deleted_at',)

    def get_content_type(self, obj):
        model_name = obj._meta.model_name
        return model_name

    def get_app_label(self, obj):
        app_label = obj._meta.app_label
        return app_label

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

    #def get_related_to_add(self, obj):
    #    return [{
    #        "model": 'indicators',
    #        "field": "SpecialOffer",
    #        "id": obj.id,
    #        "field_label": "Indicator",
    #        "hide_links": ['outcome', 'output', 'project',]
    #    }]

    def get_lookups(self, obj):
        return get_lookups_data(obj)


class SpecialOfferTableModelSerializer(serializers.ModelSerializer):
    owner = UserNameSerializer(read_only=True)
    updated_by = UserNameSerializer(read_only=True)
    is_owned = serializers.SerializerMethodField()
    
    class Meta:
        model = LOCAL_MODEL
        fields = ['created_at', 'updated_at', 'owner', "updated_by", 'name', '_id', 'id',  ]
        #exclude = ('deleted_at', 'description',)

    def get_is_owned(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user:
                return obj.owner == user
        return False

class SpecialOfferNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOCAL_MODEL
        fields = ['name',]

