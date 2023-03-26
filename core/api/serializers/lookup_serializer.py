from rest_framework import serializers

class LookupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    _id = serializers.UUIDField()
    name = serializers.CharField()


def get_lookups_data(obj):
    details = dir(obj)
    entities = []
    lookups_f = []

    for d in details:
        if '_set' in d:
            splits = d.split('_')
            if len(splits) == 1:
                continue
            if splits[0] == '':
                continue
            if splits[0] == 'geography':
                continue
            if splits[1] == 'set':
                lookups_f.append(d)
                qs = getattr(obj, d).all().order_by('pk')[:3]
                if qs.exists():
                    entities.append(
                        {
                            "model": 
                                {"name": qs.first()._meta.model_name,
                                    "app_name": qs.first()._meta.app_label
                                },
                            "data": LookupSerializer(qs, many=True).data
                        }) 
                else:
                    attr = getattr(obj, d)
                    
                    #print(attr.model)
                    entities.append(
                        {
                            "model": 
                                {"name": attr.model._meta.model_name,
                                    "app_name": attr.model._meta.app_label
                                },
                            "data": []
                        }) 
        else:
            continue
    return entities

