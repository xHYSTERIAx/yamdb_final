# Generated by Django 2.2.16 on 2022-06-13 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220613_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='lcljplvhpx', max_length=10, verbose_name='Код подтверждения'),
        ),
    ]
