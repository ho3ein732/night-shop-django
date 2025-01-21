# Generated by Django 5.1.4 on 2025-01-21 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_bannerimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerimage',
            name='banner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.banner', verbose_name='بنر'),
            preserve_default=False,
        ),
    ]
