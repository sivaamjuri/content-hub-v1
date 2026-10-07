from rest_framework import serializers
from .models import Category, ArticlePage


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category Snippet — used in protected API endpoints."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for ArticlePage — used in public listing endpoint.
    Note: full content is served via Wagtail API v2 (/api/v2/pages/).
    This DRF endpoint gives a lightweight listing view.
    """
    category = CategorySerializer(read_only=True)
    status = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = ArticlePage
        fields = ['id', 'title', 'excerpt', 'slug', 'category', 'status', 'url']

    def get_status(self, obj):
        return 'published' if obj.live else 'draft'

    def get_url(self, obj):
        return obj.full_url
