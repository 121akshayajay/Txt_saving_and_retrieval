# Generated by Django 5.0.1 on 2024-01-23 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_tag_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='content',
        ),
    ]
