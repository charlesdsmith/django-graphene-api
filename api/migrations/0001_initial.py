# Generated by Django 2.1.3 on 2018-11-06 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarFax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=20)),
                ('structural_damage', models.CharField(default='Check Online', max_length=100)),
                ('total_loss', models.CharField(default='Check Online', max_length=100)),
                ('accident', models.CharField(default='Check Online', max_length=100)),
                ('airbags', models.CharField(default='Check Online', max_length=100)),
                ('odometer', models.CharField(default='Check Online', max_length=100)),
                ('recalls', models.CharField(default='Check Online', max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('html', models.TextField(default='Check Online')),
            ],
        ),
        migrations.CreateModel(
            name='GetAdesaPurchases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=20)),
                ('vehicle_id', models.IntegerField()),
                ('vehicle_make', models.CharField(default='n/a', max_length=20)),
                ('vin_sticker', models.CharField(default='n/a', max_length=20)),
                ('auction_id', models.IntegerField()),
                ('year', models.IntegerField()),
                ('model_name', models.CharField(default='n/a', max_length=20)),
                ('mileage', models.IntegerField()),
                ('unit_of_measurement', models.CharField(default='n/a', max_length=20)),
                ('exterior_color', models.CharField(default='n/a', max_length=10)),
                ('seller_name', models.CharField(default='n/a', max_length=20)),
                ('purchase_date', models.DateTimeField(null=True)),
                ('title_status', models.CharField(default='n/a', max_length=20)),
                ('pdi_status', models.CharField(default='n/a', max_length=20)),
                ('transport_status', models.CharField(default='n/a', max_length=20)),
                ('location_name', models.CharField(default='n/a', max_length=20)),
                ('buyer_rep_name', models.CharField(default='n/a', max_length=20)),
                ('buyer_fee', models.CharField(default='n/a', max_length=20)),
                ('buyer_ad_and_other_fees', models.CharField(default='n/a', max_length=20)),
                ('fees_hst', models.CharField(default='n/a', max_length=20)),
                ('taxable_purchase_price', models.CharField(default='n/a', max_length=20)),
                ('total_hst', models.CharField(default='n/a', max_length=20)),
                ('total_price', models.CharField(default='n/a', max_length=20)),
                ('last_update_date_adesa', models.DateTimeField(null=True)),
                ('last_update_date_gsm', models.DateTimeField(null=True)),
                ('void_boolean', models.NullBooleanField(max_length=10)),
                ('payment_status', models.CharField(default='n/a', max_length=10)),
                ('amount', models.CharField(default='n/a', max_length=20)),
                ('purchase_price', models.CharField(default='n/a', max_length=20)),
                ('purchase_hst', models.CharField(default='n/a', max_length=20)),
                ('bill_of_sale', models.URLField(default='n/a')),
                ('checked', models.CharField(default='n/a', max_length=15)),
                ('recalls', models.TextField(default='n/a')),
                ('manufacturer_date', models.CharField(default='n/a', max_length=20)),
                ('gvwr', models.CharField(default='n/a', max_length=20)),
                ('gross_axle_weight_front', models.CharField(default='n/a', max_length=20)),
                ('gross_axle_weight_rear', models.CharField(default='n/a', max_length=20)),
                ('tire_size', models.CharField(default='n/a', max_length=20)),
                ('tire_pressure_front', models.CharField(default='n/a', max_length=20)),
                ('tire_pressure_rear', models.CharField(default='n/a', max_length=20)),
                ('rim_size', models.CharField(default='n/a', max_length=20)),
            ],
        ),
    ]
