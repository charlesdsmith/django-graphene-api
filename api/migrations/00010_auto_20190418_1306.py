# Generated by Django 2.1.3 on 2019-04-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190425_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getadesarunlist',
            name='grade',
            field=models.CharField(max_length=20, default='Check Online'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='check',
            field=models.CharField(max_length=20, default='Check Online'),
        ),

    ]

