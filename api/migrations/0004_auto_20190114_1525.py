# Generated by Django 2.1.3 on 2019-01-14 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190103_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='getadesarunlist',
            name='suggested_retail',
            field=models.CharField(default='Check Online', max_length=250),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='mileage',
            field=models.CharField(default='Check Online', max_length=20),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='suggested_retail',
            field=models.CharField(default='Check Online', max_length=250),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='trim',
            field=models.CharField(default='Check Online', max_length=60),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='GSMR',
            field=models.TextField(default='Check Online', max_length=250),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='MID',
            field=models.CharField(default='Check Online', max_length=250),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='MMR',
            field=models.TextField(default='Check Online', max_length=250),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='transactions',
            field=models.CharField(default='Check Online', max_length=250),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='GSMR',
            field=models.TextField(default='Check Online', max_length=250),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='MID',
            field=models.CharField(default='Check Online', max_length=250),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='MMR',
            field=models.TextField(default='Check Online', max_length=250),
        ),
    ]