# Generated by Django 2.1.3 on 2019-01-21 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20190121_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='getadesapurchases',
            name='adesa_id',
            field=models.CharField(default='n/a', max_length=20),
        ),
        migrations.AddField(
            model_name='getadesarunlist',
            name='adesa_id',
            field=models.CharField(default='n/a', max_length=20),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='adesa_id',
            field=models.CharField(default='n/a', max_length=20),
        ),
    ]