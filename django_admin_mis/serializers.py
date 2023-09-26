from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject


class AdminMenuSerializer(serializers.Serializer):
    data = serializers.JSONField()

class ActionSerializer(serializers.Serializer):
    item_ids = serializers.CharField(required=True)  # Renamed 'ids' to 'item_ids'
    action = serializers.CharField(required=True)

class DynamicSerializer(serializers.ModelSerializer):
    class Meta:
        model = None 
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        fields = kwargs.pop('fields', None)

        if not model:
            raise ValueError('The "model" parameter should not be empty.')  # Improved error message
        
        self.Meta.model = model
        if fields:
            self.Meta.fields = fields
            
        super().__init__(*args, **kwargs)
        
    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if isinstance(attribute, PKOnlyObject):
                    # Construct a dictionary with 'id' and 'value' fields for PKOnlyObject
                    value = getattr(instance, field.field_name).__str__()
                    ret[field.field_name] = {
                        'id' : field.to_representation(attribute),
                        'value' : value
                    }
                    
                else:
                    # Serialize the field normally
                    ret[field.field_name] = field.to_representation(attribute)

        return ret
