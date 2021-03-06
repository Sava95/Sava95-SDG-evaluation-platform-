# Generated by Django 3.1.1 on 2020-10-07 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_name', models.CharField(max_length=50)),
                ('goal_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'sdg_goals',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_name', models.TextField(max_length=100)),
                ('sector_code', models.CharField(max_length=10)),
                ('sector_level', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'sdg_sectors',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_code', models.CharField(max_length=10)),
                ('target_label', models.TextField(max_length=1000)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.goal')),
                ('goal_name', models.TextField(max_length=100)),
            ],
            options={
                'db_table': 'sdg_targets',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_name', models.CharField(max_length=20)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.sector')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.goal')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.target')),
                ('relevance', models.CharField(default=None, max_length=10)),
                ('location_flag', models.BooleanField(default=False)),
                ('comment', models.TextField(default=None, max_length=100)),
                ('date_posted', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'evaluations',
            },
        ),
        migrations.CreateModel(
            name='EvaluatedGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_name', models.CharField(max_length=20)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.goal')),
                ('goal_name', models.CharField(max_length=40)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.sector')),
                ('date_posted', models.DateTimeField(auto_now=True)),

            ],
            options={
                'db_table': 'evaluated_goals',
            },
        ),
    ]
