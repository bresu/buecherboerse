# Generated by Django 4.2.10 on 2024-02-23 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0012_alter_book_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Anmerkung'),
        ),
        migrations.AddField(
            model_name='seller',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Anmerkung'),
        ),
        migrations.AlterField(
            model_name='book',
            name='exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='search.exam', verbose_name='Prüfung'),
        ),
    ]
