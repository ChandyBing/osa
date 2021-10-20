from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import failure


class failureSerializer(serializers.ModelSerializer):
    class Meta:
        model = failure
        fields = '__all__'
        extra_kwargs = {
            'id': {'required': False},
            'failure_system_name': {'required': False},
            'failure_happen_time': {'required': False},
            'failure_recover_time': {'required': False},
            'keep_time': {'required': False},
            'failure_scope_batch_id': {'required': False},
            'failure_impact': {'required': False},
            'failure_level': {'required': False},
            'measure_completion_status': {'required': False},
            'affected_customer': {
                'allow_null': True,
                'allow_blank': True,
                'required': False
            },
            'affected_orders': {
                'allow_null': True,
                'allow_blank': True,
                'required': False
            },
            'affected_amount': {
                'allow_null': True,
                'allow_blank': True,
                'required': False
            },
        }
