from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .const import CHANNELS, MARKS


class Company(models.Model):
    """
    Модель компании
    атрибуты:
        company_name (str): название компании;
        slug (str): слаг(индекс) компании;
        fio (str): ФИО руководителя компании;
        description (str): Описание компании;
        published (date): Дата публикации записи;
        edited (date): Дата последнего изменения;
    """
    company_name = models.CharField(max_length=150, unique=True, verbose_name='Название компании')
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг')
    fio = models.CharField(max_length=150, verbose_name='Руководитель компании')
    description = RichTextUploadingField(blank=True, verbose_name='Описание')
    published = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    edited = models.DateField(auto_now=True, verbose_name='Последнее изменение')

    class Meta:
        ordering = ['published']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        """
        Метод класса,который возвращает строковое представление объекта Company
        :return:
        """
        return self.company_name

    def get_absolute_url(self):
        """
        Возвращает url компании с конкретным слагом
        :return:
        """
        return reverse_lazy('company-detail', kwargs={'slug': self.slug})


class Phone(models.Model):
    """
    Модель телефона
    атрибуты:
        user(class): Екземпляр класса Company
        phone(str): Номер телефона
    """
    user = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='Компания')
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')


class Email(models.Model):
    """
        Модель посты
        атрибуты:
            user(class Company): Екземпляр класса Company
            email(str): Адрес электронной почты
        """
    user = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='Компания')
    email = models.EmailField(max_length=30, verbose_name='Адрес электронной почты')


class Project(models.Model):
    """
    Модель проекта
        атрибуты:
        user(class Company): Екземпляр класса Company;
        title(str): Название проекта;
        description(str): Описание проекта;
        started_at(Date): Дата начала работы над проектом;
        finished_at(Date): Дата окончания работы над проектом;
        cost(int): Затраты на проект;
    """
    user = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='Компания')
    title = models.CharField(max_length=250, verbose_name='Название проекта')
    description = RichTextUploadingField(blank=True, verbose_name='Описание')
    started_at = models.DateField(verbose_name='Дата начала проекта')
    finished_at = models.DateField(blank=True, null=True, verbose_name='Дата завершения проекта')
    cost = models.IntegerField(blank=True, null=True, validators=(MinValueValidator(0),)
                               , verbose_name='Затраты на проект')

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """
        Метод класса,который возвращает строковое представление объекта Project
        :return:
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает url проекта с конкретным id
        :return:
        """
        return reverse_lazy('project-detail', kwargs={'pk': self.id})

    def clean(self):
        """
        Проверка вводимых дат на корректность относительно друг друга
        :return:
        """
        if (
                self.started_at and self.finished_at
                and (self.started_at > self.finished_at)
        ):
            raise ValidationError({'started_at': 'Started_at can`t be bigger then finished_at'})


class Interaction(models.Model):
    """
    Модель взаимодействия
        атрибуты:
            project(class Project): Екземпляр класса Project;
            channel(str): Канал обращения;
            manager(class User): Екземпляр класса User;
            description(str): Описание взаимодействия;
            mark(str): Выставленная оценка;
            created_at(Date): Дата создания взаимодействия;
            updated_at(Date): Дата обновления взаимодействия;

    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')

    channel = models.CharField(max_length=1, choices=CHANNELS, verbose_name='Канал обращения')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер')
    description = RichTextUploadingField(blank=True, verbose_name='Описание')

    mark = models.CharField(max_length=1, choices=MARKS, verbose_name='Оценка')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'

    def get_absolute_url(self):
        """
        Возвращает url взаимодействия с конкретным id
        :return:
        """
        return reverse_lazy('interaction-detail', kwargs={'pk': self.id})

    def __str__(self):
        """
        Метод класса,который возвращает строковое представление объекта Interaction
        :return:
        """
        return self.description


class Profile(models.Model):
    """
    Модель Profile
        атрибуты:
            user(class User): Основа профиля;
            profile_image(img): Картинка профиля;
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    profile_image = models.ImageField(verbose_name='Аватар', blank=True, null=True)

    def __str__(self):
        """
        Метод класса,который возвращает строковое представление объекта Profile
        :return:
        """
        return self.user.username
