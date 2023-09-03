# Generated by Django 2.2.19 on 2023-09-02 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_auto_20230902_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='difficulty',
            field=models.CharField(blank=True, choices=[('easy', '(легкая версия)'), ('medium', '(удобное переложение)'), ('hard', '(для опытных музыкантов)')], help_text='Выберите сложность', max_length=16, null=True, verbose_name='Сложность'),
        ),
        migrations.AlterField(
            model_name='file',
            name='difficulty',
            field=models.CharField(blank=True, choices=[('easy', '(легкая версия)'), ('medium', '(удобное переложение)'), ('hard', '(для опытных музыкантов)')], help_text='Выберите сложность', max_length=16, null=True, verbose_name='Сложность'),
        ),
    ]