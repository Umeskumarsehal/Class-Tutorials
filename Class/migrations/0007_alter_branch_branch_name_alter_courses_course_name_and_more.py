# Generated by Django 5.0.4 on 2024-06-02 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0006_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='branch_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='courses',
            name='course_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Class.branch'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='fname',
            field=models.CharField(default='Teacher', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='id_key',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='lname',
            field=models.CharField(default='', max_length=50),
        ),
    ]
