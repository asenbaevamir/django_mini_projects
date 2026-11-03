from time import timezone

from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class AuctionItem(models.Model):
    title = models.CharField(max_length=46, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
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
        null = False,
        verbose_name = "Максимально возможная цена"
    )
    buy_now_price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = False,
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

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return timezone.now > self.end_time