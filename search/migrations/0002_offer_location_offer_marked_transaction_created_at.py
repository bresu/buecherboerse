# Generated by Django 4.2.10 on 2024-02-10 22:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='location',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='marked',
            field=models.BooleanField(default=True, verbose_name='Markiert'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 10, 22, 4, 48, 947374, tzinfo=datetime.timezone.utc), verbose_name='Erstellt am'),
            preserve_default=False,
        ),
    ]
