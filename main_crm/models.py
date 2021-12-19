from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Client(models.Model):
    company_name = models.CharField(max_length=150)
    fio = models.CharField(max_length=150)
    description = RichTextUploadingField(blank=True)
    published = models.DateField(auto_now_add=True)
    edited = models.DateField(auto_now=True)

    class Meta:
        ordering = ['published']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.fio


class Phone(models.Model):
    user = models.ForeignKey('Client', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)


class Email(models.Model):
    user = models.ForeignKey('Client', on_delete=models.CASCADE)
    email = models.CharField(max_length=30)
