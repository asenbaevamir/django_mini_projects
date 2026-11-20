from django import forms
from .models import AuctionItem, Bid


class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = [
            'title',
            'description',
            'image',
            'start_price',
            'current_max_price',
            'buy_now_price',
            'start_time',
            'end_time',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'start_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_max_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'buy_now_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Введите сумму ставки'
            })
        }

    def __init__(self, *args, lot=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lot = lot

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not self.lot:
            return amount

        min_bid = self.lot.min_next_bid()
        if amount < min_bid:
            raise forms.ValidationError(
                f"Ставка должна быть не меньше {min_bid} ₽ (текущая цена {self.lot.current_price()} ₽)."
            )

        if self.lot.current_max_price and amount > self.lot.current_max_price:
            raise forms.ValidationError(
                f"Ставка не может превышать максимально возможную цену {self.lot.current_max_price} ₽."
            )

        return amount

