# Generated by Django 5.0.1 on 2024-02-10 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category_blog_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='update',
            new_name='updated',
        ),
    ]
