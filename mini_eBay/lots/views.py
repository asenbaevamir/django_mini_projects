from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuctionItemForm, BidForm
from .models import AuctionItem, Bid


def lots_list(request):
    lots = AuctionItem.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'lots/lot_list.html', {'lots': lots})


def lot_detail(request, pk):
    lot = get_object_or_404(AuctionItem.objects.prefetch_related('bids__bidder'), pk=pk)
    bid_form = BidForm(lot=lot)
    return render(request, 'lots/lot_detail.html', {
        'lot': lot,
        'bid_form': bid_form,
        'bids': lot.bids.all()[:10],
    })


@login_required
def lot_create(request):
    if request.method == 'POST':
        form = AuctionItemForm(request.POST, request.FILES)
        if form.is_valid():
            lot = form.save(commit=False)
            lot.seller = request.user
            lot.save()
            return redirect(lot.get_absolute_url())
    else:
        form = AuctionItemForm()
    return render(request, 'lots/lot_create.html', {'form': form})


@login_required
def place_bid(request, pk):
    lot = get_object_or_404(AuctionItem, pk=pk)

    if not lot.is_active or lot.is_expired:
        messages.error(request, 'Торги по этому лоту завершены.')
        return redirect(lot.get_absolute_url())

    if lot.seller == request.user:
        messages.error(request, 'Вы не можете делать ставку на свой собственный лот.')
        return redirect(lot.get_absolute_url())

    if request.method == 'POST':
        form = BidForm(request.POST, lot=lot)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.lot = lot
            bid.bidder = request.user
            bid.save()

            if lot.buy_now_price and bid.amount >= lot.buy_now_price:
                lot.is_active = False
                lot.save()
                messages.success(request, 'Поздравляем! Ваша ставка достигла цены выкупа, лот закрыт.')
            else:
                messages.success(request, f'Ставка {bid.amount} ₽ успешно принята!')
            return redirect(lot.get_absolute_url())
    else:
        form = BidForm(lot=lot)

    return render(request, 'lots/lot_detail.html', {
        'lot': lot,
        'bid_form': form,
        'bids': lot.bids.all()[:10],
    })


@login_required
def buy_now(request, pk):
    lot = get_object_or_404(AuctionItem, pk=pk)

    if not lot.is_active or lot.is_expired:
        messages.error(request, 'Торги по этому лоту завершены.')
        return redirect(lot.get_absolute_url())

    if not lot.buy_now_price:
        messages.error(request, 'Для этого лота не установлена цена выкупа.')
        return redirect(lot.get_absolute_url())

    if lot.seller == request.user:
        messages.error(request, 'Вы не можете выкупить собственный лот.')
        return redirect(lot.get_absolute_url())

    if request.method == 'POST':
        Bid.objects.create(lot=lot, bidder=request.user, amount=lot.buy_now_price)
        lot.is_active = False
        lot.save()
        messages.success(request, f'Вы успешно выкупили лот за {lot.buy_now_price} ₽!')

    return redirect(lot.get_absolute_url())

