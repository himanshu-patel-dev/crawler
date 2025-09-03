from django.contrib import admin
from .models import Page, URLRecord

@admin.register(URLRecord)
class URLRecordAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'status', 'retries', 'last_error')
    list_filter = ('status',)
    search_fields = ('url', 'last_error')

    def short_url(self, obj):
        return obj.url[:100]  # show first 100 chars
    short_url.short_description = 'URL'

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'short_title', 'short_description', 'page_type', 'topics')
    search_fields = ('title', 'description', 'url__url', 'topics')
    list_filter = ('page_type',)

    def short_url(self, obj):
        return obj.url.url[:100]
    short_url.short_description = 'URL'

    def short_title(self, obj):
        return (obj.title[:75] + '...') if obj.title and len(obj.title) > 75 else obj.title
    short_title.short_description = 'Title'

    def short_description(self, obj):
        return (obj.description[:75] + '...') if obj.description and len(obj.description) > 75 else obj.description
    short_description.short_description = 'Description'
