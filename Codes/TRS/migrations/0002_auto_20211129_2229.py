# Generated by Django 3.2 on 2021-11-29 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TRS', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='administrator',
            old_name='Balance',
            new_name='balance',
        ),
        migrations.RenameField(
            model_name='customers',
            old_name='Balance',
            new_name='balance',
        ),
    ]
