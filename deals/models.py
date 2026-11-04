from django.db import models
from clients.models import Client, Manager, Contact


class Deal(models.Model):
    class Stage(models.TextChoices):
        OPEN = 'Открыта', 'Открыта'
        WON = 'Выиграна', 'Выиграна'
        LOST = 'Проиграна', 'Проиграна'
        CANCELLED = 'Отменена', 'Отменена'

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='deals', verbose_name="Клиент"
    )
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, related_name='deals', verbose_name="Менеджер"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals', verbose_name="Контакт"
    )
    amount = models.FloatField(verbose_name="Сумма")
    title = models.CharField(max_length=250, blank=True, verbose_name="Тема")
    stage = models.CharField(
        max_length=50,
        choices=Stage.choices,
        default=Stage.OPEN,
        verbose_name="Стадия"
    )

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

    def __str__(self):
        return f"Сделка №{self.id}: {self.title} ({self.client.name})"
