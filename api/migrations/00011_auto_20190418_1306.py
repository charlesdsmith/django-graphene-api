# Generated by Django 2.1.3 on 2019-04-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '00010_auto_20190418_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='GetAdesaRunlist',
            name='grade',
            field=models.CharField(max_length=20, default='Check Online'),
        ),
        migrations.AlterField(
            model_name='ShoppingList',
            name='check',
            field=models.CharField(max_length=20, default='Check Online'),
        ),

    ]
