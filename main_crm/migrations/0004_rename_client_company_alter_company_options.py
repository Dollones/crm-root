# Generated by Django 4.0 on 2021-12-21 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_crm', '0003_client_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Client',
            new_name='Company',
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['published'], 'verbose_name': 'Company', 'verbose_name_plural': 'Companys'},
        ),
    ]
