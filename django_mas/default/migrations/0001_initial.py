# Generated by Django 5.0.6 on 2024-07-03 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='scored_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=30)),
                ('DriveTrain', models.CharField(max_length=30)),
                ('EngineSize', models.FloatField()),
                ('Cylinders', models.IntegerField()),
                ('Horsepower', models.IntegerField()),
                ('MPG_City', models.FloatField()),
                ('Weight', models.FloatField()),
                ('Wheelbase', models.IntegerField()),
                ('P_MSRP', models.FloatField()),
            ],
        ),
    ]
