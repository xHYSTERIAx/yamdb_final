# Generated by Django 2.2.16 on 2022-06-21 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0027_auto_20220621_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='lljbbpjyqh', max_length=10, verbose_name='Код подтверждения'),
        ),
    ]