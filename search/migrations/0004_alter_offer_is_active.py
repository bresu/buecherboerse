# Generated by Django 4.2.10 on 2024-02-11 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_alter_offer_wish_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Aktiv'),
        ),
    ]
