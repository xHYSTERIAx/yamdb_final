# Generated by Django 2.2.16 on 2022-06-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20220616_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='score',
            new_name='rating',
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='gqiautmrvk', max_length=10, verbose_name='Код подтверждения'),
        ),
    ]