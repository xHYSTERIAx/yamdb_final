# Generated by Django 2.2.16 on 2022-06-13 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='giplyqwmzy', max_length=10, verbose_name='Код подтверждения'),
        ),
    ]
