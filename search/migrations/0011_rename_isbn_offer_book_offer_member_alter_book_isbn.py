# Generated by Django 4.2.10 on 2024-02-21 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search', '0010_remove_offer_member_alter_exam_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='isbn',
            new_name='book',
        ),
        migrations.AddField(
            model_name='offer',
            name='member',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='FV-Mitglied'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=13, primary_key=True, serialize=False, verbose_name='ISBN'),
        ),
    ]
