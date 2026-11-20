from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class AuctionItem(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lots',
        null=True,
        blank=True,
        verbose_name="Продавец",
    )
    title = models.CharField(max_length=46, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(
        upload_to='lots/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    start_price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators = [MinValueValidator(0.01)],
        verbose_name = "Начальная (минимальная) ставка"
    )
    current_max_price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = "Максимально возможная цена"
    )
    buy_now_price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = "Цена выкупа(Купить Сразу)"
    )
    start_time = models.DateTimeField(
        default=timezone.now,
        verbose_name = "Время начала торгов"
    )
    end_time = models.DateTimeField(
        verbose_name = "Время окончания торгов"
    )

    is_active  = models.BooleanField(
        default = True
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "когда товар был создан"
    )

    def current_price(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.amount
        return self.start_price

    def min_next_bid(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.amount + 1
        return self.start_price

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lot_detail', kwargs={'pk': self.pk})

    @property
    def is_expired(self):
        return timezone.now() > self.end_time


class Bid(models.Model):
    lot = models.ForeignKey(
        AuctionItem,
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name="Лот",
    )
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name="Пользователь",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма ставки",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время ставки",
    )

    class Meta:
        ordering = ['-amount', '-created_at']

    def __str__(self):
        return f"{self.bidder} - {self.amount} ₽ ({self.lot.title})"