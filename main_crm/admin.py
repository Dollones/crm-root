from django.contrib import admin
from .models import Company, Phone, Email, Project


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


class EmailStackedInline(admin.StackedInline):
    model = Email
    extra = 0


class PhoneStackedInline(admin.StackedInline):
    model = Phone
    extra = 0


class ProjectStackedInline(admin.StackedInline):
    model = Project
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('company_name',)}
    inlines = (PhoneStackedInline, EmailStackedInline, ProjectStackedInline)
