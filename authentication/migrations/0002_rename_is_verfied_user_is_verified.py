# Generated by Django 4.2 on 2023-05-09 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_verified',
            new_name='is_verified',
        ),
    ]
