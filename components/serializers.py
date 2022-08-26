from rest_framework import serializers
from components.models import SiteRecord, ComponentPost


class SiteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteRecord
        fields = ['id', 'hostname', 'shop_site', 'xpath']


class ComponentPostSerializer(serializers.ModelSerializer):
    site_records = SiteRecordSerializer(read_only=True)

    class Meta:
        model = ComponentPost
        fields = ['id', 'site_records', 'media_url', 'page_url', 'category']
