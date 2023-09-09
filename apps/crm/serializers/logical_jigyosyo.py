from rest_framework import serializers
from ..models import LogicalJigyosyo


class LogicalJigyosyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicalJigyosyo
        fields = '__all__'
