# Generated by Django 3.0.6 on 2020-09-24 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactsapp', '0004_remove_contact_favorite_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='deceased',
            field=models.DateField(blank=True, null=True),
        ),
    ]