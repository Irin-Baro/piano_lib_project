# Generated by Django 2.2.19 on 2024-09-28 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20240716_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Продукт в корзине', 'verbose_name_plural': 'Продукты в корзинах'},
        ),
    ]
