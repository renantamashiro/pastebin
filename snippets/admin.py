from django.contrib import admin

from snippets.models import Snippet, Travel


class SnippetAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields': ['created', 'title', 'code']}),
        ('Options', {'fields': ['linenos', 'language', 'style']}),
        ('Owner', {'fields': ['owner', 'highlighted']})
    ]

    list_display = ['title', 'created', 'linenos', 'language', 'style', 'owner']
    search_fields = ['title', 'language']
    list_filter = ['style']


class TravelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic info', {'fields': ['location', 'description']}),
        ('Another', {'fields': ['country', 'date_travel']})
    ]
    
    list_display = ['location', 'description', 'country', 'date_travel']
    search_fields = ['location']
    list_filter = ['country']


admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Travel, TravelAdmin)
