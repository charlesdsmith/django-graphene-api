# Generated by Django 2.1.3 on 2019-10-02 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20190919_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='damagecomparison',
            name='adesa_id',
            field=models.TextField(default='n/a'),
        ),
        migrations.AddField(
            model_name='damagecomparison',
            name='analysis',
            field=models.TextField(default='n/a'),
        ),
        migrations.AlterField(
            model_name='damagecomparison',
            name='id',
            field=models.BigIntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]