# Generated by Django 4.1.4 on 2022-12-21 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_semester_semester_id_semester_batch_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_results_json',
        ),
        migrations.AddField(
            model_name='course',
            name='batch_no',
            field=models.CharField(default='', max_length=8),
        ),
    ]
