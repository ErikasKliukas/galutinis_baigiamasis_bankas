# Generated by Django 4.0.6 on 2022-07-13 17:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0006_transfer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Status',
            new_name='Account',
        ),
    ]
