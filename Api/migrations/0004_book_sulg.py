# Generated by Django 5.0.6 on 2024-12-16 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0003_alter_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='sulg',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]