# Generated by Django 5.0.6 on 2024-07-03 12:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_scored_data_created_alter_scored_data_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scored_data',
            name='Created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
