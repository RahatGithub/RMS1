# Generated by Django 4.1.4 on 2023-01-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.CharField(default='', max_length=200),
        ),
    ]
