# Generated by Django 3.1.1 on 2021-01-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0012_auto_20210122_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predefinedcomments',
            name='comment',
            field=models.CharField(default=None, max_length=100),
        ),
    ]