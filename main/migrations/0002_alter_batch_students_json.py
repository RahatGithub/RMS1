# Generated by Django 4.1.4 on 2022-12-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='students_json',
            field=models.CharField(default=None, max_length=5000),
        ),
    ]
