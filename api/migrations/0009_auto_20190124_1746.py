# Generated by Django 2.1.3 on 2019-01-24 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190121_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getadesarunlist',
            name='human_valuation',
            field=models.TextField(default="{'error': 'error}'"),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='human_valuation',
            field=models.TextField(default="{'error': 'error}'"),
        ),
    ]