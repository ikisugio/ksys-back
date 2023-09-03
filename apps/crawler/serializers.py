from rest_framework import serializers
from .models import CrawlList, CrawlDetail


class CrawlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlList
        fields = "__all__"


class CrawlDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlDetail
        fields = "__all__"
