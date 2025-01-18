# Generated by Django 5.1.4 on 2025-01-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_published_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='email',
            field=models.EmailField(default=0, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='first_name',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='last_name',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
