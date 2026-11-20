from django.contrib import admin

from .models import AuctionItem, Bid


class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(AuctionItem)
class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'start_price', 'buy_now_price', 'is_active', 'end_time')
    list_filter = ('is_active',)
    search_fields = ('title',)
    inlines = [BidInline]


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('lot', 'bidder', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('lot__title', 'bidder__username')
