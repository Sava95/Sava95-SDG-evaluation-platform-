# Generated by Django 3.1.1 on 2021-02-19 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_auto_20210125_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='comment_ids',
            field=models.TextField(default=None, max_length=20, null=True),
        ),
    ]
