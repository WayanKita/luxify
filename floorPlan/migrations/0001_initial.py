# Generated by Django 2.0.4 on 2018-05-03 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.CharField(max_length=2)),
                ('position', models.CharField(max_length=3)),
                ('occupied', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(max_length=2)),
                ('x_length', models.CharField(max_length=5)),
                ('y_length', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=5)),
                ('x_pos', models.CharField(max_length=5)),
                ('y_pos', models.CharField(max_length=5)),
                ('x_size', models.CharField(max_length=5)),
                ('y_size', models.CharField(max_length=5)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='floorPlan.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_pos', models.CharField(max_length=3)),
                ('end_pos', models.CharField(max_length=3)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='floorPlan.Room')),
            ],
        ),
        migrations.AddField(
            model_name='chair',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='floorPlan.Table'),
        ),
    ]