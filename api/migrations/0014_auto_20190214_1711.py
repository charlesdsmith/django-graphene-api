# Generated by Django 2.1.3 on 2019-02-14 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20190207_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='grade',
            field=models.CharField(default='Check Online', max_length=20),
        ),
    ]