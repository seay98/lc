# Generated by Django 3.0.6 on 2020-05-21 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basesite',
            name='cell_idle_srxlev',
            field=models.BigIntegerField(),
        ),
    ]
