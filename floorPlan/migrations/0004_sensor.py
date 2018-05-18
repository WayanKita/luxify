# Generated by Django 2.0.4 on 2018-05-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floorPlan', '0003_auto_20180504_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
                ('date', models.DateTimeField()),
                ('value', models.FloatField()),
            ],
        ),
    ]