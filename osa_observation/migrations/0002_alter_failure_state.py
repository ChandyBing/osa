# Generated by Django 3.2 on 2021-10-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osa_observation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failure',
            name='state',
            field=models.IntegerField(default=0, verbose_name='填写状态'),
        ),
    ]
