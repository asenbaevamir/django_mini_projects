from django.contrib import admin

from .models import AuctionItem


@admin.register(AuctionItem)
class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_price', 'buy_now_price', 'is_active', 'end_time')
    list_filter = ('is_active',)
    search_fields = ('title',)
