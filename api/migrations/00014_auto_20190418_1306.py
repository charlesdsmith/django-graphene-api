# Generated by Django 2.1.3 on 2019-04-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '00013_auto_20190418_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='grade',
            field=models.TextField(default='n/a'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='check',
            field=models.TextField(default='n/a'),
        ),

    ]

