# Generated by Django 3.1.1 on 2021-06-18 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0032_auto_20210615_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='esaveprojects',
            name='esave_source_of_fund_ID',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
