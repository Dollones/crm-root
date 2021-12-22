from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse_lazy


class Company(models.Model):
    company_name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, null=True)
    fio = models.CharField(max_length=150)
    description = RichTextUploadingField(blank=True)
    published = models.DateField(auto_now_add=True)
    edited = models.DateField(auto_now=True)

    class Meta:
        ordering = ['published']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse_lazy('company-detail', kwargs={'company_slug': self.slug})


class Phone(models.Model):
    user = models.ForeignKey('Company', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)


class Email(models.Model):
    user = models.ForeignKey('Company', on_delete=models.CASCADE)
    email = models.CharField(max_length=30)
