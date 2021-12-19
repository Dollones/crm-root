from django.contrib import admin
from .models import Client, Phone, Email


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass


class PhoneStackedInline(admin.StackedInline):
    model = Phone
    extra = 0


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass


class EmailStackedInline(admin.StackedInline):
    model = Email
    extra = 0


class PhoneStackedInline(admin.StackedInline):
    model = Phone
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = (PhoneStackedInline, EmailStackedInline)
