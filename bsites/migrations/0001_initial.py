# Generated by Django 3.0.6 on 2020-05-21 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basesite',
            fields=[
                ('rs', models.IntegerField()),
                ('addresses', models.TextField()),
                ('num_mnc_digits', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('ul_bandwidth', models.IntegerField()),
                ('ci1', models.IntegerField()),
                ('mcc', models.IntegerField()),
                ('ci2', models.CharField(max_length=100)),
                ('deviceId', models.CharField(max_length=128)),
                ('lac', models.IntegerField()),
                ('dl_bandwidth', models.IntegerField()),
                ('freq_band_ind', models.IntegerField()),
                ('creatTime', models.DateTimeField()),
                ('serv_rssnr', models.IntegerField()),
                ('cell_rsrp', models.IntegerField()),
                ('pci', models.IntegerField()),
                ('tac', models.IntegerField()),
                ('cell_rsrq', models.IntegerField()),
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('earfcn', models.IntegerField()),
                ('longitude', models.FloatField()),
                ('serving_cell_id', models.IntegerField()),
                ('mnc', models.IntegerField()),
                ('ch', models.IntegerField()),
                ('cell_pci', models.IntegerField()),
                ('nonce', models.IntegerField()),
                ('userId', models.CharField(max_length=128)),
                ('cell_idle_srxlev', models.IntegerField()),
                ('cell_rssi', models.IntegerField()),
                ('reportTime', models.DateTimeField()),
            ],
        ),
    ]
