# Generated by Django 2.2.16 on 2022-06-21 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0024_auto_20220621_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='bcchnuwlqg', max_length=10, verbose_name='Код подтверждения'),
        ),
    ]
