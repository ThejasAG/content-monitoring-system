from rest_framework import serializers
from .models import Keyword, ContentItem, Flag

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']

class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['id', 'title', 'body', 'source', 'last_updated']

class FlagSerializer(serializers.ModelSerializer):
    keyword_name = serializers.CharField(source='keyword.name', read_only=True)
    content_item_title = serializers.CharField(source='content_item.title', read_only=True)

    class Meta:
        model = Flag
        fields = [
            'id', 'keyword', 'keyword_name', 'content_item', 
            'content_item_title', 'score', 'status', 
            'created_at', 'last_reviewed_at'
        ]
        read_only_fields = ['score', 'created_at']

class FlagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ['status', 'last_reviewed_at']
