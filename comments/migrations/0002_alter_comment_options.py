# Generated by Django 5.1.4 on 2025-01-10 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_date'], 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
    ]
