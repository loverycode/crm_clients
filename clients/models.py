from django.db import models
from datetime import date


class Client(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    status = models.CharField(
        max_length=50, default="Новый", verbose_name="Статус")
    created = models.DateField(
        default=date.today, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['name']

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(max_length=256, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Contact(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Клиент"
    )
    name = models.CharField(max_length=256, verbose_name="Имя контакта")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    position = models.CharField(
        max_length=100, blank=True, verbose_name="Должность")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.name} ({self.client.name})"
