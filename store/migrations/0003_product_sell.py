# Generated by Django 5.1.4 on 2025-01-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_favoriteproduct_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell',
            field=models.IntegerField(default=0, verbose_name='تعداد فروش'),
        ),
    ]
