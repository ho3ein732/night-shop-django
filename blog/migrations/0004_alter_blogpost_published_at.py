# Generated by Django 5.1.4 on 2025-01-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogpost_slug_alter_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='published_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ انتشار'),
        ),
    ]
