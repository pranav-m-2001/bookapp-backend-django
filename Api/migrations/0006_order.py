# Generated by Django 5.0.6 on 2024-12-18 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0005_rename_sulg_book_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.JSONField(default=list, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.JSONField(default=dict, null=True)),
                ('status', models.CharField(default='Order placed', max_length=100)),
                ('paymentMethod', models.CharField(max_length=100)),
                ('payment', models.BooleanField(default=False)),
                ('ordered_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='Api.userprofile')),
            ],
        ),
    ]
