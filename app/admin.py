from django.contrib import admin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "source", "is_featured", "user")
    list_filter = ("is_featured", "created_date")
    search_fields = ("text", "author", "source")
