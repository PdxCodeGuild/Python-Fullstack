# Generated by Django 3.0.6 on 2020-09-23 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactsapp', '0003_contact_favorite_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='favorite_color',
        ),
    ]
