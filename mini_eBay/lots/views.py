from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuctionItemForm
from .models import AuctionItem


def lots_list(request):
    lots = AuctionItem.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'lots/lot_list.html', {'lots': lots})


def lot_detail(request, pk):
    lot = get_object_or_404(AuctionItem, pk=pk)
    return render(request, 'lots/lot_detail.html', {'lot': lot})


def lot_create(request):
    if request.method == 'POST':
        form = AuctionItemForm(request.POST)
        if form.is_valid():
            lot = form.save()
            return redirect(lot.get_absolute_url())
    else:
        form = AuctionItemForm()
    return render(request, 'lots/lot_create.html', {'form': form})

