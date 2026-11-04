from django.contrib import admin
from .models import Deal
from clients.models import Client, Manager, Contact
from django import forms


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'phone', 'position')
    search_fields = ('name', 'phone', 'client__name')
    list_filter = ('client',)


class DealInline(admin.TabularInline):
    model = Deal
    extra = 1
    fields = ('client', 'title', 'amount', 'stage', 'manager')
    can_delete = False

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            # Скрываем поле client и подставляем текущего клиента
            formset.form.base_fields['client'].widget = forms.HiddenInput()
            formset.form.base_fields['client'].initial = obj
        return formset


@admin.register(Client)
class ClientAdminWithDeals(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'is_vip', 'created')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('status', 'is_vip')
    ordering = ('name',)
    inlines = [DealInline]


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'client', 'manager', 'amount', 'stage')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'client__name', 'manager__name')
    list_filter = ('stage', 'manager')
    ordering = ('-id',)
    list_per_page = 20
