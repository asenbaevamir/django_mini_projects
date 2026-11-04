from django.shortcuts import get_object_or_404, render

from .models import AuctionItem


def lots_list(request):
    lots = AuctionItem.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'lot_list.html', {'lots': lots})


def lot_detail(request, pk):
    lot = get_object_or_404(AuctionItem, pk=pk)
    return render(request, 'lot_detail.html', {'lot': lot})
