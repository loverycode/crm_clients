from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from datetime import date


class Client(models.Model):
    class Status(models.TextChoices):
        NEW = 'Новый', 'Новый'
        IN_PROGRESS = 'В работе', 'В работе'
        CLOSED = 'Закрыт', 'Закрыт'
        REJECTED = 'Отказ', 'Отказ'

    name = models.CharField(max_length=256, verbose_name="Название")
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус"
    )
    created = models.DateField(
        default=date.today, verbose_name="Дата создания")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        editable=False,
        verbose_name="URL-идентификатор"
    )
    is_vip = models.BooleanField(
        default=False,
        verbose_name="VIP-клиент"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "client"
            self.slug = f"{base_slug}-{self.pk or 'new'}"

        super().save(*args, **kwargs)

        if self.slug.endswith('-new'):
            self.slug = self.slug.replace('-new', f'-{self.pk}')
            super().save(update_fields=['slug'])

        if self.pk:
            from deals.models import Deal  # Импорт внутри, чтобы избежать циклов
            has_won_deal = self.deals.filter(stage=Deal.Stage.WON).exists()
            if self.is_vip != has_won_deal:
                self.is_vip = has_won_deal
                super().save(update_fields=['is_vip'])

    def get_absolute_url(self):
        return reverse("clients:detail", kwargs={"slug": self.slug})

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
