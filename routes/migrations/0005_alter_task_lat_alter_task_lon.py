# Generated by Django 5.1.2 on 2025-05-14 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0004_rename_tasks_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='lon',
            field=models.FloatField(),
        ),
    ]
