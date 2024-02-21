# Generated by Django 4.2.10 on 2024-02-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_rename_isactive_offer_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=13, unique=True, verbose_name='ISBN')),
                ('title', models.CharField(max_length=100, verbose_name='Titel')),
                ('authors', models.CharField(max_length=100, verbose_name='Autoren')),
                ('maxPrice', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Maximaler Preis')),
                ('edition', models.IntegerField(verbose_name='Auflage')),
                ('publisher', models.CharField(max_length=30, verbose_name='Verlag')),
                ('exam', models.CharField(choices=[('EXAM_1', 'FÜM1'), ('EXAM_2', 'FÜM2'), ('EXAM_3', 'Exam 3'), ('EXAM_4', 'Exam 4'), ('EXAM_5', 'Exam 5'), ('EXAM_6', 'Exam 6'), ('EXAM_7', 'Exam 7'), ('EXAM_8', 'Exam 8'), ('EXAM_9', 'Exam 9'), ('EXAM_10', 'Exam 10'), ('EXAM_11', 'Exam 11'), ('EXAM_12', 'Exam 12'), ('EXAM_13', 'Exam 13'), ('EXAM_14', 'Exam 14'), ('EXAM_15', 'Exam 15'), ('EXAM_16', 'Exam 16'), ('EXAM_17', 'Exam 17')], max_length=20, verbose_name='Prüfung')),
            ],
        ),
        migrations.CreateModel(
            name='ExamModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.CharField(choices=[('EXAM_1', 'FÜM1'), ('EXAM_2', 'FÜM2'), ('EXAM_3', 'Exam 3'), ('EXAM_4', 'Exam 4'), ('EXAM_5', 'Exam 5'), ('EXAM_6', 'Exam 6'), ('EXAM_7', 'Exam 7'), ('EXAM_8', 'Exam 8'), ('EXAM_9', 'Exam 9'), ('EXAM_10', 'Exam 10'), ('EXAM_11', 'Exam 11'), ('EXAM_12', 'Exam 12'), ('EXAM_13', 'Exam 13'), ('EXAM_14', 'Exam 14'), ('EXAM_15', 'Exam 15'), ('EXAM_16', 'Exam 16'), ('EXAM_17', 'Exam 17')], default='EXAM_1', max_length=20)),
            ],
        ),
    ]