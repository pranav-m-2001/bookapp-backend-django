# Generated by Django 5.0.6 on 2024-12-22 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0007_userprofile_dob_userprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wishlist',
            field=models.JSONField(default=list, null=True),
        ),
    ]
