from rest_framework import serializers
from ..models import Jigyosyo


class JigyosyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jigyosyo
        fields = "__all__"
