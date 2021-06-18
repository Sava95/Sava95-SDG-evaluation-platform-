# Generated by Django 3.1.1 on 2021-06-18 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0033_esaveprojects_esave_source_of_fund_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoF',
            fields=[
                ('esave_source_of_fund_ID', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=100)),
                ('esave_bank_ID', models.CharField(default=None, max_length=100)),
            ],
            options={
                'db_table': 'xxx_esave_source_of_funds',
            },
        ),
    ]
