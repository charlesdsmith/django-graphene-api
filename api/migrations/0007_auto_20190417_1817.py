# Generated by Django 2.1.3 on 2019-04-17 22:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190417_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getadesarunlist',
            name='MMR',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='check',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
