from django.contrib import admin
from .models import Keyword, ContentItem, Flag

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'last_updated')
    search_fields = ('title', 'body', 'source')

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'content_item', 'score', 'status', 'created_at', 'last_reviewed_at')
    list_filter = ('status', 'created_at', 'keyword')
    search_fields = ('keyword__name', 'content_item__title')
    readonly_fields = ('created_at', 'score')
