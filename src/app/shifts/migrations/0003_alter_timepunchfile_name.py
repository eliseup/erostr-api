# Generated by Django 5.2.4 on 2025-07-24 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0002_timepunchfile_code_timepunchfile_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timepunchfile',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
