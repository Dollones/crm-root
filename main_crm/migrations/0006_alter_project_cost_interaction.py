# Generated by Django 4.0 on 2021-12-24 11:11

import ckeditor_uploader.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main_crm', '0005_alter_company_options_alter_company_company_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cost',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.CharField(choices=[('r', 'Заявка'), ('l', 'Письмо'), ('w', 'Сайт'), ('i', 'Инициатива компании')], max_length=1)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('mark', models.CharField(choices=[('1', 'Ужасно'), ('2', 'Плохо'), ('3', 'Нормально'), ('4', 'Хорошо'), ('5', 'Отлично')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_crm.project')),
            ],
            options={
                'verbose_name': 'Interaction',
                'verbose_name_plural': 'Interactions',
                'ordering': ['-updated_at'],
            },
        ),
    ]
