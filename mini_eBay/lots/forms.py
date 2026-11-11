from django import forms
from .models import AuctionItem


class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = [
            'title',
            'description',
            'start_price',
            'current_max_price',
            'buy_now_price',
            'start_time',
            'end_time',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_max_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'buy_now_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

