# Generated by Django 4.1.4 on 2022-12-18 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.CharField(default='', max_length=18)),
                ('batch_no', models.CharField(default='', max_length=6)),
                ('session', models.CharField(default='', max_length=8)),
                ('students_json', models.CharField(default='', max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(default='', max_length=20)),
                ('course_code', models.CharField(default='', max_length=8)),
                ('course_title', models.CharField(default='', max_length=60)),
                ('course_type', models.CharField(default='', max_length=10)),
                ('course_credits', models.FloatField(default=0)),
                ('course_teacher', models.CharField(default='', max_length=40)),
                ('course_results_json', models.CharField(default='', max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_id', models.CharField(default='', max_length=14)),
                ('semester_no', models.IntegerField(default=None)),
                ('courses_json', models.CharField(default='', max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_no', models.CharField(default='', max_length=10)),
                ('batch_no', models.CharField(default='', max_length=6)),
                ('session', models.CharField(default='', max_length=8)),
                ('name', models.CharField(default='', max_length=60)),
                ('father_name', models.CharField(default='', max_length=60)),
                ('mother_name', models.CharField(default='', max_length=60)),
                ('address', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=11)),
                ('isResidential', models.BooleanField(default=False)),
                ('isCR', models.BooleanField(default=False)),
                ('average_cgpa', models.FloatField(default=0)),
                ('remarks', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
