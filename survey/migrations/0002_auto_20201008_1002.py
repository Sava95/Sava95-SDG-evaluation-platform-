# Generated by Django 3.1.1 on 2020-10-08 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluatedgoal',
            name='goal_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='comment',
            field=models.TextField(default=None, max_length=200),
        ),
    ]
