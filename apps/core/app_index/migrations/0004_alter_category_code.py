# Generated by Django 5.1.6 on 2025-07-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_index', '0003_category_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='code',
            field=models.CharField(blank=True, default='', help_text='Clé technique unique (ex: artiste, compilation, label, lexique, etc.).', max_length=50, null=True, verbose_name='Code'),
        ),
    ]
