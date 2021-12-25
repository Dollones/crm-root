from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse_lazy
from django.contrib.auth.models import User


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
        return self.company_name

    def get_absolute_url(self):
        return reverse_lazy('company-detail', kwargs={'company_slug': self.slug})


class Phone(models.Model):
    user = models.ForeignKey('Company', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)


class Email(models.Model):
    user = models.ForeignKey('Company', on_delete=models.CASCADE)
    email = models.EmailField(max_length=30)


class Project(models.Model):
    user = models.ForeignKey('Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = RichTextUploadingField(blank=True)
    started_at = models.DateField()
    finished_at = models.DateField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True, validators=(MinValueValidator(0),))

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.id})

    def clean(self):
        if (
                self.started_at and self.finished_at
                and (self.started_at > self.finished_at)
        ):
            raise ValidationError({'started_at': 'Started_at can`t be bigger then finished_at'})


class Interaction(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    CHANNELS = (
        ('r', 'Заявка'),
        ('l', 'Письмо'),
        ('w', 'Сайт'),
        ('i', 'Инициатива компании'),
    )

    channel = models.CharField(max_length=1, choices=CHANNELS)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=True)

    MARKS = (
        ('1', 'Ужасно'),
        ('2', 'Плохо'),
        ('3', 'Нормально'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    )

    mark = models.CharField(max_length=1, choices=MARKS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'

    def get_absolute_url(self):
        return reverse_lazy('interaction-detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.description


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField()

    def __str__(self):
        return self.user.username